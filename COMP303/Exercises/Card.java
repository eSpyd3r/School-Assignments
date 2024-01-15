public class Card implements Comparable<Card>
{
	private Optional<Rank> aRank;
	private Optional<Suit> aSuit;
	private Optional<Joker> aJoker;

	private enum Joker {WHITE, BLACK}

	public Card(Rank pRank, Suit pSuit) {
		assert pRank != null && pSuit != null;
		aRank = Optional<Rank>.of(pRank);
		aSuit = Optional<Suit>.of(pSuit);
		aJoker = Optional<Joker>.empty();
	}

	/**
	 * Constructor of Joker card
	 * 
	 * @param pJoker color Joker to assign
	 * 
	 * @pre pJoker != null
	 */

	public Card(boolean isWhite) {
		aRank = Optional<Rank>.empty();
		aSuit = Optional<Suit>.empty();

		if (isWhite) {aJoker = Optional<Joker>.of(Joker.WHITE);}
		else {aJoker = Optional<Joker>.of(Joker.BLACK);}
	}

	public Rank getRank() {
		assert aRank.isPresent() && aJoker.isEmpty();
		return aRank.get();
	}

	public Suit getSuit() {
		assert aSuit.isPresent() && aJoker.isEmpty();
		return aSuit.get();
	}

	public boolean isJoker {return aJoker.isPresent();}
	public boolean isWhiteJoker {return isJoker() && (aJoker.get() == Joker.WHITE);}
	public boolean isBlackJoker {return isJoker() && (aJoker.get() == Joker.BLACK);}

	@Override
	public int compareTo(Card pCard) {return aRank.compareTo(pCard.aRank);}

	public static Comparator<Card> createByRankComparator() {
		return new Comparator<Card>() {

			@Override
			public int compare(Card pCard1, Card pCard2) {
				if (pCard1.aJoker.isEmpty() && pCard2.aJoker.isEmpty()) {return pCard1.aRank.compareTo(pCard2.aRank);}
				else if (!pCard1.aJoker.isEmpty() && pCard2.aJoker.isEmpty()) {return 1}
				else if (pCard1.aJoker.isEmpty() && !pCard2.aJoker.isEmpty()) {return -1};
				else {return pCard1.aJoker.get().ordinal() - pCard2.aJoker.get().ordinal()}
			}
		}
	}

	@Override
	public boolean equals(Object pObject) {
		if (pObject == this) {return true;}
		else if (pObject == null) {return false;}
		else if(pObject.getClass() != getClass()) {return false;}
		else {
			return ((Card)pObject.aRank == aRank && (Card)pObject.aSuit == aSuit);
		}
	}

	@Override
	public int hashChode() {return aSuit.ordinal() * Rank.values().length + aRank.ordinal()}
}







