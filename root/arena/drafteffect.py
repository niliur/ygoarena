class DraftEffect():

	effects = 9

	@staticmethod
	def getDraftEffects():
		effArray = []
		effArray.append((0, "No Effect"))
		effArray.append((1, "If you pick this card, get 2 copies of it"))
		effArray.append((2, "If you pick this card, draft 1 more main deck card"))
		effArray.append((3, "If you pick this card, draft 3 more main deck cards"))
		effArray.append((4, "If you pick this card, draft 2 less main deck cards"))
		effArray.append((5, "If you pick this card, draft 1 more extra deck card"))
		effArray.append((6, "If you pick this card, get 1 token"))
		effArray.append((7, "If you pick this card, your next card draft has only 4 options"))
		effArray.append((8, "If you pick this card, get 2 tokens"))
		effArray.append((9, "If you pick this card, lose 1 token"))

		return effArray