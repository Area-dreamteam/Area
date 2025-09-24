/*
** EPITECH PROJECT, 2025
** Area_Mirroring
** File description:
** page
*/

export default function Home()
{
  return (
    <div className="bg-[#000000] h-screen">
      <div className="bg-[#0518c5] h-5/7">
        <h1 className="flex justify-center text-[100px]">Area</h1>
        <h2 className="flex justify-center text-[25px]">Build your own chain of reactions</h2>
        <div className="flex justify-center">
          <button className="bg-[#FFFFFF] text-[#000000] hover:bg-[#73bbff] rounded-xl w-[150px] h-[50px]">
            Start now
          </button>
        </div>
      </div>
    </div>
  );
}
