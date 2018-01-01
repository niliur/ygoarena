export class Deck{

	public hash: string; // Min 10 Chars
	public mainDeck: number;
	public extraDeck: number;
	public mainDeckLimit : number;
	public extraDeckLimit : number;
	public size: number;
	public bonusid: number;
	public characterid: number;

	public finished: boolean;
	public draftFinished: boolean;
	public tokens : number;


	constructor(jsonObject: any){
		this.hash = jsonObject.hashField;

		this.mainDeck = jsonObject.mainDeck;
		this.extraDeck = jsonObject.extraDeck;
		this.mainDeckLimit = jsonObject.mainDeckLimit;
		this.extraDeckLimit = jsonObject.extraDeckLimit;
		this.size = jsonObject.size;
		this.bonusid = jsonObject.bonusid;
		this.characterid = jsonObject.characterid;
		this.finished = jsonObject.finished;
		this.draftFinished = jsonObject.draftFinished;
		this.tokens = jsonObject.tokens;
	}
}