import { Component } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/toPromise';


@Component({
	selector: 'app-root',
	templateUrl: './app.component.html',
	styleUrls: ['../assets/css/app.component.css']
})

export class AppComponent {
	title = 'app';

}