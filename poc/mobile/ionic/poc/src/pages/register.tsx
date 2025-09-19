import { IonButton, IonContent, IonHeader, IonInput, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import './register.css';

function Register() {
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Register</IonTitle>
        </IonToolbar>
      </IonHeader>

      <IonContent fullscreen>
        <div className="login-container">
          <IonInput
            label='email'
            labelPlacement='floating'
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
          <IonButton routerLink="/isRegisted">
            Register
          </IonButton>
          <IonButton routerLink='/login'>
            Login
          </IonButton>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default Register;