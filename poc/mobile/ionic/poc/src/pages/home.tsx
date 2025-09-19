import { IonText, IonButton } from '@ionic/react';

function Home() {
  return (
    <>
      <div>
        <IonButton href='/login'>
          <p>Login</p>
        </IonButton>
        <IonButton href='/register'>
          <p>Register</p>
        </IonButton>
      </div>
    </>
  );
}
export default Home;
