
'use client'

import Warning from '@/app/components/Warning'
import { Input } from '@/components/ui/input'
import { useEffect, use, useState } from 'react'
import { notFound, useRouter } from 'next/navigation'
import ValidateButton from '@/app/components/Validation'
import { AppletRespSchema, PrivateApplet, SpecificPrivateApplet } from '@/app/types/applet'
import {
  fetchPrivateApplet,
  fetchPersonalApplets,
  fetchUpdatePersonalApplets,
} from '@/app/functions/fetch'
import { Act, ActDetails } from '@/app/types/service'
import AppletManagement from '@/app/components/appletManagement'

type AppletProp = {
  params: Promise<{ slug: string }>
}

async function editApplet(
  title: string,
  desc: string,
  oldApplet: SpecificPrivateApplet
) {
  if (title == '' || desc == '') return false
  const modifiedApplet: AppletRespSchema = {
    name: title,
    description: desc,
    action: {
      action_id: oldApplet.action.id,
      config: oldApplet.action.config,
    },
    reactions: oldApplet.reactions.map((reac) => {
      return {
        reaction_id: reac.id,
        config: reac.config,
      }
    }),
  }
  await fetchUpdatePersonalApplets(modifiedApplet, oldApplet.area_info.id)
  return true;
}

export default function Edit({ params }: AppletProp) {
  const slug = use(params).slug;
  const [loading, setLoading] = useState(true)
  const [applets, setApplets] = useState<PrivateApplet[] | null>(null)
  const [myApplet, setMyApplet] = useState<SpecificPrivateApplet | null>(null)
  const [currApplet, setCurrApplet] = useState<PrivateApplet | undefined>(undefined)
  const [editingAppletParameters, setEditingAppletParameters] = useState<boolean>(false);
  const [appletConfig, setAppletConfig] = useState<AppletRespSchema | null>(null);
  const [theReactions, setTheReactions] = useState<ActDetails[] | null>(null);
  const [theAction, setTheAction] = useState<ActDetails | null>(null);
  const [title, setTitle] = useState<string>('')
  const [desc, setDesc] = useState<string>('')
  const router = useRouter();

  useEffect(() => {
    const loadApplets = async () => {
      await fetchPersonalApplets(setApplets)
    }
    loadApplets()
  }, [])

  useEffect(() => {
    if (applets != null) {
      const searched = applets.find(
        (applet) => applet.id == Number(slug)
      )
      setCurrApplet(searched)

      if (!searched) setLoading(false)
    }
  }, [applets])

  useEffect(() => {
    if (currApplet) fetchPrivateApplet(setMyApplet, currApplet.id)
  }, [currApplet])

  useEffect(() => {

    function getReactions(applet: SpecificPrivateApplet)
    {
      let nb = 1;
      const reactions: ActDetails[] = applet.reactions.map((reac) => {
        const act: Act = {
          id: reac.id,
          name: reac.name,
          description: reac.description
        }
        const reaction: ActDetails = {
          id: nb,
          config: reac.config,
          act: act
        }
        nb += 1;
        return reaction;
      });
      return reactions;
    }
  
    if (myApplet != null) {
      setLoading(false);
      setTitle(myApplet.area_info.name);
      setDesc(myApplet.area_info.description);
      const act: Act = {
        id: myApplet.action.id,
        name: myApplet.action.name,
        description: myApplet.action.description
      }
      const action: ActDetails = {
        id: 0,
        config: myApplet.action.config,
        act: act
      }
      setTheAction(action);
      setTheReactions(getReactions(myApplet));
    }
  }, [myApplet])

  useEffect(() => {
    if (!appletConfig || !myApplet) {
      setEditingAppletParameters(false);
      setAppletConfig(null);
      return;
    }
    const updateArea = async () => {
      await fetchUpdatePersonalApplets(appletConfig, myApplet.area_info.id);
      router.push("/my_applets");
    }
    updateArea();
  }, [appletConfig])

  if ((!currApplet || !myApplet) && !loading)
    notFound();

  return (
    <div style={{ background: myApplet?.area_info.color }}>
      {loading
        ? ('Loading'
        ) : (
        myApplet &&
          !editingAppletParameters ? (
            <div className="py-[50px] h-screen w-[75%] mx-auto">
              <Input
                aria-label="This input allow you to change the title of the applet"
                className="centered subtitle bg-white"
                defaultValue={myApplet.area_info.name}
                placeholder="Title"
                onChange={(e) => setTitle(e.target.value)}
              />
              <hr className="mt-[25px] mb-[25px]" />
              <textarea
                aria-label="you can change the description of your applet here"
                className="rounded-md bg-white text-black w-[75%] h-[20%] px-[1%] mx-auto block"
                defaultValue={
                  myApplet.area_info.description
                    ? myApplet.area_info.description
                    : ''
                }
                placeholder="description"
                minLength={1}
                onChange={(e) => setDesc(e.target.value)}
                required
              />
              <br />
              <p className="simple-text inverted w-[75%] block mx-auto">
                Created by: {myApplet.area_info.user.name}
                <br />
                At:{' '}
                {new Date(myApplet.area_info.created_at).toLocaleDateString()}
              </p>
              <br />
              <button className="rounded-button block mx-auto mt-[10%]" onClick={() => setEditingAppletParameters(true)}>
                Change Applet's configuration
              </button>
              <ValidateButton
                clickAct={() => {
                  const status = editApplet(title, desc, myApplet);
                  if (!status)             
                    return Warning('Update impossible', '');
                  router.push(`/my_applets`);
                }}
                arg={true}
                text="Validate"
                addToClass="mt-[20%]"
              />
            </div>
          ) : (
            <div className="h-max pb-[5%]">
              <AppletManagement 
                creating={false}
                theAction={theAction}
                setTheAction={setTheAction}
                theReactions={theReactions}
                setTheReactions={setTheReactions}
                setAppletRespSchema={setAppletConfig}
              />
            </div>
          )
        )
      }
    </div>
  )
}
