public class Hand implements Comparable<Hand>, Iterable<Card> {

	private List<Card> aCards;
	private int aMaxNumCards;
	private Comparator<Card> aComparator;
	private PokerHand aPokerHand = PokerHand.HIGHCARD;
	enum PokerHand {HIGHCARD, PAIR, TWOPAIR...}

	/**
	 * Constructor for a hand
	 * 
	 * @param pMaxNumCards maximum number of cards in a hand
	 * @pre pMaxNumCards > 0
	 */

	public Hand(int pMaxNumCards) {
		assert pMaxNumCards > 0;

		aCards = new ArrayList<>(pMaxNumCards);
		aMaxNumCards = pMaxNumCards;
	}

	public Hand(int pMaxNumCards, Comparator<Hand> pComparator) {
		assert pMaxNumCards > 0 && pComparator != null;

		aCards = new ArrayList<>(pMaxNumCards);
		aMaxNumCards = pMaxNumCards;
		aComparator = pComparator;
	}


	public void getHandStrength() {
		//insert PokerHand check logic
	}

	/**
	 * Adds card to hand
	 * 
	 * @param pCard card to add
	 * 
	 * @pre pCard != null
	 * @pre !isFull()
	 * @pre !contains(pCard)
	 */
	public void add(Card pCard) {
		assert pCard != null;
		assert !isFull();
		assert !contains(pCard);

		aCards.add(pCard);
		aCards.sort(aComparator);
	}


	/**
	 * Removes card from hand
	 * 
	 * @param pCard card to remove
	 * 
	 * @pre pCard != null
	 * @pre !isEmpty()
	 * @pre contains(pCard)
	 */
	public void remove(Card pCard) {
		assert pCard != null;
		assert !isEmpty();
		assert contains(pCard);

		aCards.remove(pCard);
	}

	/**
	 * Checks if hand contains pCard
	 * 
	 * @param pCard card to check
	 * 
	 * @pre pCard != null
	 */
	public boolean contains(Card pCard) {
		assert pCard != null;

		return aCards.contains(pCard);
	}

	/**
	 * Checks if hand is empty
	 */
	public boolean isEmpty() {
		return aCards.isEmpty();
	}

	/**
	 * Returns number of cards in the hand
	 */
	public int size() {
		return aCards.size();
	}

	/**
	 * Checks if hand is full
	 */
	public boolean isFull() {
		return aMaxNumCards == this.size();
	}  

	/**
	 * returns an unmodifiable view of the cards in the hand
	 */
	public List<Card> getCards() {
		return Collections.unmodifiableList(aCards);
	}

	/**
	 * Establishes comparison of hands by increasing number of cards in hand
	 */
	@Override
	public int compareTo(Hand pHand) {
		return this.size().compareTo(pHand.size());
	}

	public Comparator<Hand> createIncreaseByHandSizeComparator() {
		return new Comparator<Hand>() {

			@Override
			public int compare(Hand pHand1, Hand pHand2) {
				return pHand1.size() - pHand2.size();
			}
		};
	}

	public Comparator<Hand> createDecreaseByHandSizeComparator() {
		return new Comparator<Hand>() {

			@Override
			public int compare(Hand pHand1, Hand pHand2) {
				return pHand2.size() - pHand1.size();
			}
		};
	}

	@Override
	public Iterator<Card> iterator() {
		return aCards.iterator();
	}

	public Comparator<Hand> createByIncreasingNumberOfRankComparator(Rank pRank) {
		return new Comparator<Hand>() {

			@Override
			public int compare(Hand pHand1, Hand pHand2) {
				return countRank(pHand, pRank) - countRank(pHand2, pRank);
			}

			public int countRank(Hand pHand, Rank pRank) {
				int count = 0;
				for(Card card : pHand) {
					if (card.getRank() == pRank) {count++;}
				}

				return count;
			}
		}
	}



}






