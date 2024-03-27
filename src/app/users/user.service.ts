import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Signup } from '../pages/login/login.component';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient) { }

  registerUser(userData: Signup){
    return this.http.post<any>('http://127.0.0.1:8000/api/user/register/',userData);
  }}
