import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { Http, Response, RequestOptions, Headers } from '@angular/http';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import 'rxjs/add/operator/toPromise';

import {AppSettings} from '../app-settings';

import { Deck } from '../deck';
import {DeckBonusSelector, DeckBonus, DeckSize, DeckSizeSelector} from '../deck-options';

@Component({
	selector: 'app-deck-form',
	templateUrl: './deck-form.component.html',
	styleUrls: ['./deck-form.component.css'],
})

export class DeckFormComponent implements OnInit {
	private loadDeckForm: FormGroup;
	private submittedHash: boolean;
	private events: any[] = [];
	private deckModel : Deck;

	private createurl : string = AppSettings.API_ENDPOINT + '/arena/deck/create';
	private loadurlstart : string = AppSettings.API_ENDPOINT + '/arena/deck/';
	private loadurlend : string = '/load';

	private requestSent: boolean;
	private deckData: JSON;
	private createDeckSuccessful: boolean = false;
	private loadDeckStatus: string;
	private getDeckStatus: string;

	private deckBonuses: DeckBonus[];
	private selectedBonus: DeckBonus;

	private deckSizes: DeckSize[];
	private selectedDeckSize : DeckSize;

	constructor(private http : Http, private db: FormBuilder, private router: Router){	}

	private loadDeck(model: Deck, isValid: boolean ){
		this.submittedHash = true;
		this.http
			.get(`${this.loadurlstart}${model.hash}${this.loadurlend}`).toPromise()
			.then(response => {
				console.log(response)
				this.submittedHash = false;
				this.loadDeckStatus = String(response.status);

				var deckdata = response.json();

				this.deckModel = new Deck(deckdata.hashField, deckdata.finished, deckdata.size,deckdata.mainDeck);

			}).catch(response =>{
				this.submittedHash = false;
				this.loadDeckStatus = String(response.status);

			});
	}

	private gotoDrafts(model: Deck){
		this.router.navigate(['/draft', model.hash]);
	}



	private createDeck(){
		this.requestSent = true;
		var obj = {};
		obj['bonusid'] = this.selectedBonus.bonusid;
		obj['decksizeid'] = this.selectedDeckSize.decksizeid;
		var data = JSON.stringify(obj);
		var headers = new Headers({ 'Content-Type': 'application/json' });
		var options = new RequestOptions({ headers: headers });
	    this.http
	    	.post(this.createurl,data, options).toPromise()
	    	.then(response => {
	    	console.log(response.status);
	    	this.requestSent = false;
	    	this.createDeckSuccessful = true;
	    	var deckdata = response.json();
	    	this.deckModel = new Deck(deckdata.hashField, deckdata.finished, deckdata.size, deckdata.mainDeck);
		  }).catch(response =>{
		  	this.requestSent = false;
		  	this.getDeckStatus = response.status;
		  });
	}

	ngOnInit() {
		this.loadDeckForm = this.db.group({
			hash: ['', [<any>Validators.required, <any>Validators.minLength(10), <any>Validators.maxLength(10)]]
		});

		var decksl = new DeckBonusSelector();
		this.deckBonuses = decksl.getBonuses();

		var decksz = new DeckSizeSelector();
		this.deckSizes = decksz.getDeckSizes();
		

		this.subcribeToFormChanges();
	}



	subcribeToFormChanges() {
	    // initialize stream
	    const myFormValueChanges$ = this.loadDeckForm.valueChanges;

	    // subscribe to the stream 
	    myFormValueChanges$.subscribe(x => this.events
	        .push({ event: 'STATUS CHANGED', object: x }));
	}

}
