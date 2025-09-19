import { IonButton, IonContent, IonHeader, IonInput, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import './login.css';

export default function Login() {
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Connexion</IonTitle>
        </IonToolbar>
      </IonHeader>

      <IonContent fullscreen>
        <div className="login-container">
          <IonInput
            label="Email"
            labelPlacement="floating"
            type="email"
            fill="outline"
            className="input-field"
          />
          <IonInput
            label="Password"
            labelPlacement="floating"
            type="password"
            fill="outline"
            className="input-field"
          />

          <IonButton routerLink="/isLogged">
            Login
          </IonButton>

          <IonButton routerLink="/register" color="secondary">
            Register
          </IonButton>
        </div>
      </IonContent>
    </IonPage>
  );
}
