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
				"1x Eidos the Underworld Squire\n" +
				"1x Double Summon"),
			new DeckBonus(6, "Trap God",
				"I ACTIVATE MY TRRRRRRAP CARD",
				"Includes:\n"+
				"1x Powerful Rebirth\n" + 
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
				"(EFFECT) You must draft 70 main deck cards ( Just choose anything for decksize) WARNING THIS SHIT DOESNT ACTUALLY WORK RIGHT NOW IN YGOPERCY"),
			new DeckBonus(99, "Nothing",
				"Play the draft without starter cards",
				""
				)];

	getBonuses(): DeckBonus[] {
		return DeckBonusSelector.bonusArray;
	}
}

export class DeckCharacter {

		constructor(
		public characterid: number,
		public name: string,
		public flavor: string,
		public desc: string,
		){}

}

export class DeckCharacterSelector {

	private static bonusArray: DeckCharacter[] = [ 
			new DeckCharacter(0, "Battle City Kaiba",
				"\"It's not a monster, it's a god! \"",
				"Includes:\n"+
				"1x Enemy Controller\n" + 
				"1x Obelisk the Tormentor\n" + 
				"1x Soul Exchange"),
			new DeckCharacter(1, "Blue Eyes Fanatic Kaiba",
				"Don't stand between a man and his dragon",
				"Includes:\n"+
				"(DRAFT EFFECT) You can always draft Blue Eyes White dragon during a maindeck draft.\n"),
			new DeckCharacter(2, "Joey",
				"A normal man with some normal cards",
				"Includes:\n"+
				"1x Red Eyes Black Dragon\n" + 
				"1x Heart of the Underdog\n" + 
				"1x Ancient Rules\n" +
				"(DRAFT EFFECT) Normal monsters will always have > 1500 atk or defense"),
			new DeckCharacter(3, "Yung Yugi",
				"It's not cheating if you're the king of games",
				"Includes:\n"+
				"1x Monster Reborn\n" + 
				"1x Horn of Heaven\n" + 
				"(EFFECT) Your deck size is 24 main deck, 6 extra deck"),
			new DeckCharacter(4, "Jaden",
				"NEEDS CONTENT",
				"Includes:\n"+
				"1x A Hero Lives\n" + 
				"1x E Hero Bubbleman\n" + 
				"1x E Hero Shadowmist\n" + 
				"1x E Hero Clayman\n" +
				"(DRAFT EFFECT) You can draft mask change during a main deck draft\n" +
				"(DRAFT EFFECT) You can draft mask change II during an extra deck draft\n" +
				"(DRAFT EFFECT) You can draft Masked Heroes during the extra deck draft"),
			new DeckCharacter(5, "The Pharaoh",
				"I also want to possess an elementary schooler",
				"Includes:\n"+
				"1x Eternal Soul\n" + 
				"1x Dark Magician\n" + 
				"1x Wonder Wand\n" +
				"(DRAFT EFFECT) 15% chance for every monster to be a spellcaster"),
			new DeckCharacter(6, "Yuma",
				"NEEDS CONTENT",
				"Includes:\n"+
				"1x Number 39 Utopia (EXTRA)\n" + 
				"(EFFECT) You can draft twice the number of extra deck monsters"),
			new DeckCharacter(7, "Mako Tsunami",
				"His cards never get wet..",
				"Includes:\n"+
				"1x Umi\n" + 
				"1x Umiruka\n" + 
				"1x A Legendary Ocean\n" + 
				"(DRAFT EFFECT) 50% chance for each monster to be WATER ATTRIBUTE"),
			new DeckCharacter(8, "Aki",
				"Konami more plant support plz",
				"Includes:\n"+
				"1x Lonefire Blossom\n" + 
				"1x Glow-up Bulb\n" + 
				"1x Blue Rose Dragon\n" +
				"1x Gigaplant\n" + 
				"1x Black Rose Dragon(EXTRA)"),
			new DeckCharacter(99, "Nothing",
				"Play the draft without starter cards",
				""
				)];

	getCharacters(): DeckCharacter[] {
		return DeckCharacterSelector.bonusArray;
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
		new DeckSize(0, "32 Main Deck, 8 Extra Deck",
			"For the man on the go"),
		new DeckSize(1, "40 Main Deck, 10 Extra Deck",
			"Old reliable"),
		new DeckSize(2, "48 Main Deck, 12 Extra Deck",
			"A well balanced deck with a well balanced breakfast")
	];

	getDeckSizes(): DeckSize[] {
		return DeckSizeSelector.deckSizeArray;
	}
}