import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { Http, Response, RequestOptions, Headers } from '@angular/http';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Router, ActivatedRoute} from '@angular/router';
import 'rxjs/add/operator/toPromise';


import { Deck } from '../deck';
import {Draft} from '../draft';
import {Card} from '../card';
import {CardType} from '../card-type.enum'
import {Text} from '../text';






import {AppSettings} from '../app-settings';


@Component({
  selector: 'app-draft-view',
  templateUrl: './draft-view.component.html',
  styleUrls: ['./draft-view.component.css'],
})


export class DraftViewComponent implements OnInit {

  private drafted : Draft[] = [];

  private draftedMDM : Draft[] = undefined;
  private draftedEDM : Draft[] = undefined;
  private draftedSpell : Draft[] = undefined;
  private draftedTrap : Draft[] = undefined;
  private draftedFiltered : Draft[] = undefined;
  private filter : string  = 'ALL';
  private order : string = 'DRAFT';


  private draftHovered : Draft = undefined;


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

  private deckModel: Deck = undefined;

  private draftSent : boolean = false;
  private finishedSent : boolean = false;


  private sub : any = undefined;


  constructor(private http : Http, private route: ActivatedRoute) {  }

  private generateFilteredDrafted(){

    if(this.order === 'DRAFT'){
      this.drafted = this.drafted.sort((a,b)=> a.picknum - b.picknum);
    }
    else if(this.order === 'ALPHABETICAL'){
      this.drafted = this.drafted.sort(function(a,b){
        if (a.text.name < b.text.name){
          return -1;
        }else if(a.text.name == b.text.name){
          return 0;
        }else return 1;
      });
    }

    if(this.filter === 'ALL'){
      this.draftedFiltered = this.drafted;
    }
    else if(this.filter === 'MDM'){
      this.draftedMDM = this.drafted.filter(e=>e.card.typeEnum === CardType.MDM);
      this.draftedFiltered = this.draftedMDM;
    }
    else if(this.filter === 'EDM'){
      this.draftedFiltered = this.draftedEDM = this.drafted.filter(function(e, i, array){
        return e.card.typeEnum === CardType.EDM;
      });
    }
    else if(this.filter === 'SPELL'){
      this.draftedFiltered = this.draftedSpell = this.drafted.filter(function(e, i, array){
        return e.card.typeEnum === CardType.Spell;
      });
    }
    else if(this.filter === 'TRAP'){
      this.draftedFiltered = this.draftedTrap = this.drafted.filter(function(e, i, array){
        return e.card.typeEnum === CardType.Trap;
      });
    }

  }

  private getDrafted(){
    this.http
    .get(`${this.loadurlstart}${this.deckCode}${this.loadDraft}`).toPromise()
    .then(response => {

      var deckdata = response.json();
      var tmpDrafts : Draft[] = [];
      for(let i = 0; i < deckdata.length; ++i){
        var draft = new Draft(deckdata[i],`${this.cardAssetUrl}${deckdata[i].card.id}.png` );
        tmpDrafts.push(draft);

      }
      this.drafted = tmpDrafts;
      this.draftedMDM = undefined;
      this.draftedEDM = undefined;
      this.draftedSpell = undefined;
      this.draftedTrap = undefined;
      this.generateFilteredDrafted();
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

  private postNoPurchase(){

    this.draftSent = true;
    var obj = {};
    obj['id'] = 0;
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
        var draft = new Draft(deckdata[i], `${this.cardAssetUrl}${deckdata[i].card.id}.png` );
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

      this.deckModel = new Deck(deckdata);
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

  private loadHoverDraft(draft : Draft){
    this.draftHovered = draft;
  }

  private clearHoverDraft(){
    this.draftHovered = undefined;
  }


  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
         this.deckCode = params['key']; // (+) converts string 'id' to a number

         this.updateDeck();


         // In a real app: dispatch action to load the details here.
       });


  }

  createRange(number){
    var items: number[] = [];
    number = Math.ceil(number);
    for(var i = 1; i <= number; i++){
      items.push(i);
    }
    return items;
  }

  

}
