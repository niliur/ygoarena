import {Card} from './card'
import {Text} from './text'

export class Draft {

	constructor(

		public id : number,
		public card : Card,
		public text : Text,
		public draftnum : number,
		public imagePath ?: string, 


	){}
}
