public class SponsoredConcert extends Concert{
	private String aSponsorName;
	private int aSponsorTime;

	public SponsoredConcert(String pTitle, String pPerformer, int pTime, String pSponsorName, int pSponsorTime) {
		super(pTitle, pPerformer, pTime);
		aSponsorName = pSponsorName;
		aSponsorTime = pSponsorTime;
	}

	@Override
	public String description() {
		return(String.format("%s sponsored by %s", super.description(), aSponsorName));
	}

	@Override
	public int time() {
		return super.time() + aSponsorTime;
	}

	@Override
	public SponsoredConcert clone() {
		SponsoredConcert clone = (SponsoredConcert) super.clone();
		return clone;
	}


}

public abstract class AbstractShow implements Show {
	protected String aTitle;
	protected int aTime;

	protected AbstractShow(String pTitle, int pTime) {
		aTitle = pTitle;
		aTime = pTime;
	}

	public String title() {return aTitle;}
	public int time() {return aTime;}
	public void setTime(int pTime) {aTime = pTime;}
	public void setTitle(String pTitle) {aTitle = pTitle;}

	public String description() {String.format("%s: %s (%d minutes)", title(), extra(), time())}
	protected abstract String extra();

	@Override
	public AbstractShow clone() {
		AbstractShow clone = (AbstractShow) super.clone();
		return clone;
	}



}

