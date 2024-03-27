import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastrModule } from 'ngx-toastr';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../../users/user.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, HttpClientModule, ToastrModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  loginObj: Login;
  // signupUsers: any[] = [];
  signupobj: Signup;
  tableData: any;

  constructor(private http: HttpClient, private router: Router, private toastr: ToastrService, private userService: UserService) {
    this.loginObj = new Login();
    this.signupobj = new Signup();
  }


  onLogin() {
    this.http.post('http://127.0.0.1:8000/api/user/login/', this.loginObj).subscribe((res: any) => {
      if (res.msg === 'Login successfully') {
        // alert("login successfull")
        this.toastr.success('Login Successful!', 'Welcome');
        this.router.navigateByUrl('/splash');
        setTimeout(() => {
          this.router.navigateByUrl('/dashboard');
        }, 5000);
      } else {
        // alert(res.message)
        this.toastr.error('Invalid login credentials!');
      }
    })
  }

  onSignup() {
    this.userService.registerUser(this.signupobj)
      .subscribe((res: any) => {
        if (res.msg === 'your registration is successfully complited') {
          this.toastr.success('Registration Successful!', 'Welcome');
          // Update table data (explained later)
          this.updateTableData(this.signupobj); // Call a function to add user data to table
          this.router.navigateByUrl('/dashboard'); // navigate to dashboard
        } else {
          this.toastr.error('Registration failed!', res.message);
        }
      });
  }

   // Function to update table data (explained later)
   updateTableData(userData: Signup) {

    this.tableData.push(userData); // Add the new user to the table data

    // Add logic to update your table data source with the new user data (userData)
    // This might involve adding the user object to an array or updating a state management service.
  }
}
export class Login {

  email: string;
  password: string;

  constructor() {
    this.email = '';
    this.password = '';
  }
}

export class Signup {
  email: string;
  name: string;
  phone: string;
  password: string;
  password2: string;
  date_of_birth: string;
  gender: string;
  address: string;

  constructor() {
    this.email = '';
    this.name = '';
    this.phone = '';
    this.password = '';
    this.password2 = '';
    this.date_of_birth = '';
    this.gender = '';
    this.address = '';
  }

}

