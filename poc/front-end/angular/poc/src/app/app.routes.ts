import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { App } from './app';
import { Login } from './login/login';
import { Logged } from './logged/logged';
import { Registering } from './registering/registering';

export const routes: Routes = [
    { path: '', component: Login, pathMatch: 'full' },
    { path: 'home', component: App },
    { path: 'logged', component: Logged },
    { path: 'registering', component: Registering },
    { path: '**', redirectTo: '/home' }
];
