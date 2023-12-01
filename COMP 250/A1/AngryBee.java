package BeeShit;

public class AngryBee extends HoneyBee {
    private int atk;

    public AngryBee(Tile position, int atk) {
        super(position, 10, 1);
        this.atk = atk;
    }

    public boolean takeAction() {
        if (!this.getPosition().isOnThePath() && !this.getPosition().isHive()) {
            System.out.println("Where the hell are you rn");
            return false;
        }

        if (this.getPosition().getHornet() != null) {
            System.out.println("There's a bitchass on my tile");
            this.getPosition().getHornet().takeDamage(atk);
            return true;
            }

       boolean hunt = true;
       Tile checkPosition = this.getPosition();
       while (hunt) {
           System.out.println("Hunting...");
           try {
               checkPosition = checkPosition.towardTheNest();
               if (checkPosition.getHornet() != null) {
                   checkPosition.getHornet().takeDamage(atk);
                   //checkPosition = this.getPosition();
                   return true;
               }
           } catch (NullPointerException e) { //once reaching the end, that is, towardThenNest = null
                hunt = false;
               }
           }

        System.out.println("Major L taken. Can't find shit");
        return false;
    }

    public boolean equals(Object obj) {
        return (obj instanceof AngryBee && ((AngryBee) obj).getHealth() == this.getHealth() &&
                ((AngryBee) obj).getPosition() == this.getPosition());
    }
}
