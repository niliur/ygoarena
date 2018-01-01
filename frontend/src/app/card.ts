export class Card {


	public id : number;
	public ot : number;
	public alias : number;
	public setcode : number;
	public type: number;
	public atk: number;
	public def: number;
	public level: number;
	public race: number;
	public attribute: number;
	public category: number;

	constructor(jsonObject : any){
		this.id = jsonObject.id;
		this.ot = jsonObject.ot;
		this.alias = jsonObject.alias;
		this.setcode = jsonObject.setcode;
		this.type = jsonObject.type;
		this.atk = jsonObject.atk;
		this.def = jsonObject.def_field;
		this.level = jsonObject.level;
		this.race = jsonObject.race;
		this.attribute = jsonObject.attribute;
		this.category = jsonObject.category;

	}


}
