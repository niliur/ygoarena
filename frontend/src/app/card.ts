import {CardType} from './card-type.enum'

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
	public typeString : string;
	public typeEnum : CardType;
	public attributeString : string;

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
		this.typeString = Card.typeToText(this.type);
		this.typeEnum = Card.typeToEnum(this.type);
		this.attributeString = Card.attributeToText(this.attribute);

	}	


	private static bitComp(code : number, value : number): boolean{
		if((code & value) === value){
			return true;
		}
		return false;

	}

	private static typeToText(code: number): string{


		if(Card.bitComp(code, 8193) || Card.bitComp(code, 65) || Card.bitComp(code, 8388609)){
			return "Extra Deck Monster"
		}
		else if(Card.bitComp(code, 1)){
			return "Main Deck Monster";
		}
		else if(Card.bitComp(code, 2)){
			return "Spell";
		}else if(Card.bitComp(code, 4)){
			return "Trap";
		}
		return "Something has gone wrong";
	}


	private static typeToEnum(code: number): CardType{


		if(Card.bitComp(code, 8193) || Card.bitComp(code, 65) || Card.bitComp(code, 8388609)){
			return CardType.EDM;
		}
		else if(Card.bitComp(code, 1)){
			return CardType.MDM;
		}
		else if(Card.bitComp(code, 2)){
			return CardType.Spell;
		}
		else if(Card.bitComp(code, 4)){
			return CardType.Trap;
		}
		return CardType.Undefined;
	}

	private static attributeToText(code){
		if(code === 0){
			return undefined;
		}
		else if((code&1) == 1){
			return "Earth";
		}
		else if((code&2) == 2){
			return "Water";
		}
		else if((code&4) == 4){
			return "Fire";
		}
		else if((code&8) == 8){
			return "Wind";
		}
		else if((code&16) == 16){
			return "Light";
		}
		else if((code&32) == 32){
			return "Dark";
		}
		else if((code&64) == 64){
			return "Divine";
		}

		return "Something has gone wrong, please report this.";
	}


} 
