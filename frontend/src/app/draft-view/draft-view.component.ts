import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { Http, Response, RequestOptions, Headers } from '@angular/http';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Router, ActivatedRoute} from '@angular/router';
import 'rxjs/add/operator/toPromise';

import { Deck } from '../deck';
import {Draft} from '../draft';
import {Card} from '../card';
import {Text} from '../text';

import {AppSettings} from '../app-settings';

@Component({
  selector: 'app-draft-view',
  templateUrl: './draft-view.component.html',
  styleUrls: ['./draft-view.component.css'],
})


export class DraftViewComponent implements OnInit {

	private drafted : Draft[] = [];


	private drafting : Draft[] = [];

	private deckCode : string;
	private loadDeckStatus : boolean;
	private loadurlstart : string = AppSettings.API_ENDPOINT + '/arena/deck/';
	private loadDraft: string = '/drafts';
	private loadDrafting: string = '/drafting';
	private loadDeck: string = '/load';
	private postFinish: string = '/finish';
	private generate: string = '/generate';

	private cardAssetUrl: string = '/assets/cards/';

	private deckExists: boolean;
	private deckFinished : boolean;

	private deckModel: Deck;

	private draftSent : boolean = false;
	private finishedSent : boolean = false;


	private sub : any;
	constructor(private http : Http, private route: ActivatedRoute) { }

	private getDrafted(){
			this.http
			.get(`${this.loadurlstart}${this.deckCode}${this.loadDraft}`).toPromise()
			.then(response => {

				var deckdata = response.json();
				var tmpDrafts : Draft[] = [];
				for(let i = 0; i < deckdata.length; ++i){
					var draft = new Draft(deckdata[i].card.id, new Card(deckdata[i].card.id), 
										new Text(deckdata[i].text.name, deckdata[i].text.desc),
										deckdata[i].draftnum);
					tmpDrafts.push(draft);

					//console.log(deckdata[i].text.name);

					//console.log(deckdata[i].text.desc);

				}
				this.drafted = tmpDrafts;
				this.loadDeckStatus = true;



			}).catch(response =>{
				this.loadDeckStatus = false;

			});
	}

	private onFinished(){
		this.draftSent = true;
		this.finishedSent = true;
	}

	private postDraft(code: number){

		this.draftSent = true;
		var obj = {};
		obj['id'] = code;
		var data = JSON.stringify(obj);
		var headers = new Headers({ 'Content-Type': 'application/json' });
		var options = new RequestOptions({ headers: headers });
	    this.http
	    	.post(`${this.loadurlstart}${this.deckCode}${this.loadDrafting}`, data, options).toPromise()
	    	.then(response => {
	    		this.updateDeck();
	    		this.draftSent = false;
		  }).catch(response =>{
		  	this.draftSent = false;
		  });
	}

	private finishDraft(){
		this.finishedSent = true;
		var obj = {};
		obj['finish'] = true;
		var data = JSON.stringify(obj);
		var headers = new Headers({ 'Content-Type': 'application/json' });
		var options = new RequestOptions({ headers: headers });
	    this.http
	    	.post(`${this.loadurlstart}${this.deckCode}${this.postFinish}`, data, options).toPromise()
	    	.then(response => {
	    		this.deckFinished = true;
		  }).catch(response =>{
		  	this.finishedSent = false;
		  });
	}

	private download(){

		window.open( this.loadurlstart + this.deckCode + this.generate, "_blank");

	}

	private getDrafting(){


		this.http
		.get(`${this.loadurlstart}${this.deckCode}${this.loadDrafting}`).toPromise()
		.then(response => {

			var deckdata = response.json();
			var tmpDrafts : Draft[] = [];
			for(let i = 0; i < deckdata.length; ++i){
				var draft = new Draft(deckdata[i].card.id, new Card(deckdata[i].card.id), 
									new Text(deckdata[i].text.name, deckdata[i].text.desc),
									deckdata[i].draftnum, `${this.cardAssetUrl}${deckdata[i].card.id}.png` );
				tmpDrafts.push(draft);

			}
			console.log(tmpDrafts);
			this.drafting = tmpDrafts;



		}).catch(response =>{

		});
	}



	private updateDeck(){
		this.http
			.get(`${this.loadurlstart}${this.deckCode}${this.loadDeck}`).toPromise()
			.then(response => {
				this.deckExists = true;

				var deckdata = response.json();

				this.deckModel = new Deck(deckdata.hashField, deckdata.finished, deckdata.size, deckdata.mainDeck);
				this.deckFinished = deckdata.finished;
				this.getDrafted();
				if(!this.deckFinished){
					this.getDrafting();
				}
				else{
					this.onFinished();
				}

			}).catch(response =>{
				this.deckExists = false;

			});
	}


	ngOnInit() {
		this.sub = this.route.params.subscribe(params => {
	       this.deckCode = params['key']; // (+) converts string 'id' to a number

	       this.updateDeck();


	       // In a real app: dispatch action to load the details here.
	    });


	}

}
