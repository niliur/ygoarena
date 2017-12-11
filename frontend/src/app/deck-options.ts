export class DeckBonus {

		constructor(
		public bonusid: number,
		public name: string,
		public flavor: string,
		public desc: string,
		){}

}

export class DeckBonusSelector {

	private static bonusArray: DeckBonus[] = [ 
			new DeckBonus(0, "Obliterate!",
				"Dominate your enemies with the ultimate alternate win condition",
				"Includes:\n"+
				"1x Pieces of Exodia (5 Total)\n" + 
				"1x Dark factory of Mass Production\n" + 
				"1x Battle Fader"),
			new DeckBonus(1, "Mech Rebellion",
				"Man vs Machine, who would win?",
				"Includes:\n"+
				"1x Raigeki\n" + 
				"1x Cyber Dragon\n" + 
				"1x Limiter Removal\n" + 
				"1x Twin Barrel Dragon"),
			new DeckBonus(2, "Unlimited Blade Works",
				"Not really unlimited, in fact the number of blades is quite limited",
				"Includes:\n"+
				"1x Axe of fools\n" + 
				"1x Butterfly Dagger: Elma\n" + 
				"1x Cursed Armaments\n" +
				"1x Iron Blacksmith Kotetsu\n" + 
				"1x Powertool Dragon (EXTRA)"),
			new DeckBonus(3, "Light Brigade",
				"Protip: don't chain Honest to Honest",
				"Includes:\n"+
				"1x White Dragon Wyverburster\n" + 
				"1x Honest\n" + 
				"1x Ryko, Lightsworn Hunter\n" +
				"1x Raiden, Hand of the Lightsworn"),
			new DeckBonus(4, "The Degenerate",
				"Battle damage is too unsophisticated for the educated Yugioh player",
				"Includes:\n"+
				"1x Wavemotion Cannon\n" + 
				"1x Nightmare wheel\n" + 
				"1x Pot of Greed\n" +
				"1x Traphole"),
			new DeckBonus(5, "Tributes",
				"Say no to rank 4 spam, get your vanity's fiend today",
				"Includes:\n"+
				"1x Tribute burial\n" + 
				"1x The monarchs stormforth\n" + 
				"1x Eidos the Underworld Squire\n" +
				"1x Double Summon"),
			new DeckBonus(6, "Trap God",
				"I ACTIVATE MY TRRRRRRAP CARD",
				"Includes:\n"+
				"1x Powerful Rebirth\n" + 
				"1x Quaking Mirror Force\n" + 
				"(EFFECT) During the draft, your spells are replaced by trap cards"),
			new DeckBonus(7, "San Sangan",
				"Stop staring at me",
				"Includes:\n"+
				"3x Sangan\n" + 
				"1x Tour Guide From the Underworld\n" + 
				"1x Ghostrick Alucard (EXTRA)\n" + 
				"1x Wind-Up Zenmaines(EXTRA)"),
			new DeckBonus(8, "Grass is Greener",
				"You have way too much free time, do something with your life",
				"Includes:\n"+
				"3x That grass looks greener ( Lawnmowing next door) \n" + 
				"1x Edge Imp Sabres\n" + 
				"1x Plaguespreader zombie\n" +
				"1x Electromagnetic turtle\n" + 
				"1x Shaddoll Beast\n" +
				"(EFFECT) You must draft 70 main deck cards ( Just choose anything for decksize)"),
			new DeckBonus(99, "Nothing",
				"Play the draft without starter cards",
				""
				)];

	getBonuses(): DeckBonus[] {
		return DeckBonusSelector.bonusArray;
	}
}

export class DeckSize {
	constructor(
		public decksizeid: number,
		public name: string,
		public desc: string,
	){}
}

export class DeckSizeSelector {
	private static deckSizeArray: DeckSize[] = [
		new DeckSize(0, "40 Main Deck, 10 Extra Deck",
			"Old reliable, sometimes less is more"),
		new DeckSize(1, "48 Main Deck, 12 Extra Deck",
			"More cards for a well-rounded deck"),
		new DeckSize(2, "60 Main Deck, 15 Extra Deck",
			"Even if I lose, my d*ck is still bigger than yours!")
	];

	getDeckSizes(): DeckSize[] {
		return DeckSizeSelector.deckSizeArray;
	}
}