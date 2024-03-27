import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { LayoutComponent } from './pages/layout/layout.component';
import { LoginComponent } from './pages/login/login.component';
import { SplashScreenComponent } from './pages/splash-screen/splash-screen.component';
import { UsersComponent } from './pages/users/users.component';

export const routes: Routes = [
    {
        path: '', redirectTo: 'login', pathMatch: 'full'
    },
    {
        path: 'splash',
        component: SplashScreenComponent
    },
    {
        path: 'login',
        component: LoginComponent
    },
    {
        path:'',
        component: UsersComponent,
        children:[
            {
                path:'dashboard',
                component: DashboardComponent
            },
            {
                path:'users',
                component: UsersComponent
            }
        ]
    }
];
