import { IonPage, IonContent, IonText } from '@ionic/react';

export default function IsLogged() {
  return (
    <IonPage>
      <IonContent className="ion-text-center ion-padding">
        <IonText color="primary">
          <h1>Logged</h1>
        </IonText>
      </IonContent>
    </IonPage>
  );
}
