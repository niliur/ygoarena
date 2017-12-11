import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';


import { AppComponent } from './app.component';
import { DeckFormComponent } from './deck-form/deck-form.component';
import { DraftViewComponent } from './draft-view/draft-view.component';


const appRoutes: Routes = [
	{ path: 'draft/:key',
	component: DraftViewComponent,
	data: {title: 'Draft'}
	},
	{ path: '',
	component: DeckFormComponent,
	data: {title: 'Deck Selection'}
	}
];


@NgModule({
declarations: [
    AppComponent,
    DeckFormComponent,
    DraftViewComponent,
],
imports: [
    BrowserModule,
    HttpModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    )
],
providers: [],
bootstrap: [AppComponent]
})
export class AppModule { }