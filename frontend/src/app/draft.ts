import {Card} from './card'
import {Text} from './text'

export class Draft {

	public id : number;
	public card : Card;
	public text : Text;
	public draftnum : number;
	public tokenCost : number;
	public imagePath ?: string;
	constructor(jsonObject: any, imgPath: string){
		this.id = jsonObject.card.id;

		this.card = new Card(jsonObject.card);
		this.text = new Text(jsonObject.text.name, jsonObject.text.desc);
		this.draftnum = jsonObject.draftnum;
		this.tokenCost = jsonObject.tokenCost;
		this.imagePath = imgPath;
	}
}
