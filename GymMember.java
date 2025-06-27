//Abstract Superclass
public abstract class GymMember
{
    //Declaring the attributes
    protected int id;
    protected String name;
    protected String location;
    protected String phone;
    protected String email;
    protected String gender;
    protected String DOB;
    protected String membershipStartDate;
    protected int attendance;
    protected double loyaltyPoints;
    protected boolean activeStatus;
    
    //Creating Constructor with parameters
    public GymMember(int id, String name, String location, String phone, String email, String gender, String DOB, String membershipStartDate)
    {
        //Assigning parameter values to respective attributes
        this.id = id;
        this.name = name.trim();
        this.location = location.trim();
        this.phone = phone.trim();
        this.email = email.trim();
        this.gender = gender;
        this.DOB = DOB;
        this.membershipStartDate = membershipStartDate;
        this.attendance = 0;
        this.loyaltyPoints = 0.0;
        this.activeStatus = false;
    }
    
    //Accessor Methods for all the attributes
    public int getId(){
        return this.id;
    }
    
    public String getName(){
        return this.name;
    }
    
    public String getLocation(){
        return this.location;
    }
    
    public String getPhone(){
        return this.phone;
    }
    
    public String getEmail(){
        return this.email;
    }
    
    public String getGender(){
        return this.gender;
    }
    
    public String getDOB(){
        return this.DOB;
    }
    
    public String getMembershipStartDate(){
        return this.membershipStartDate;
    }
    
    public int getAttendance(){
        return this.attendance;
    }
    
    public double getLoyaltyPoints(){
        return this.loyaltyPoints;
    }
    
    public boolean getActiveStatus(){
        return this.activeStatus;
    }
    
    
    //Abstract Method to mark the attendance
    public abstract void markAttendance();
    
    //Method to activate membership
    public void activateMembership(){
        
        //Condition to check if the membership is already active
        if(!this.getActiveStatus()){
            this.activeStatus = true;
        }

    }
    
    //Method to deactivate membership
    public void deactivateMembership(){
        
        //Condition to check if the membership has been deactivated already
        if(this.getActiveStatus()){
            this.activeStatus = false;
        }
    }
    
    //Resets the member status and attendance
    public void resetMember(){
        this.activeStatus = false;
        this.attendance = 0;
        this.loyaltyPoints = 0.0;
    }
    
    //Method to display all the member details
    public void display(){
        
        System.out.printf("%-5s %-20s %-20s %-15s %-25s %-30s %-30s %-30s %-20s %-25s %-10s",
        this.getId(), this.getName(), this.getLocation(), this.getPhone(), this.getEmail(),
        this.getGender(), this.getDOB(), this.getMembershipStartDate(),
        this.getAttendance(), this.getLoyaltyPoints(), this.getActiveStatus());
    }
}
