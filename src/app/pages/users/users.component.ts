import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { VoidTableComponent } from '../../reusable/void-table/void-table.component';

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [FormsModule, HttpClientModule, CommonModule, VoidTableComponent],
  templateUrl: './users.component.html',
  styleUrl: './users.component.css'
})
export class UsersComponent implements OnInit {

  usersArray: any[] = [];
  columnArray: any[] = [
    {header: 'Name', fieldName:'name', dataType:'string'},
    {header: 'User Name', fieldName:'username', dataType:'string'},
    {header: 'Email', fieldName:'email', dataType:'string'},
    {header: 'Phone No', fieldName:'phone', dataType:'string'},
    {header: 'Website', fieldName:'website', dataType:'string'},
    {header: 'Date', fieldName:'currentDate', dataType:'date'},

  ];
  constructor(private http: HttpClient){}

  ngOnInit(): void {
    this.getUsers();
  }
  
  getUsers(){
    this.http.get("http://127.0.0.1:8000/api/user/register/").subscribe((res:any)=>{
      this.usersArray = res;
      this.usersArray.forEach(element=>{
        element.currentDate = new Date()
      });
    })
  }

  editUser(data: any){
    debugger;
  }

  deleteUser(data: any){
    debugger;
  }
}
