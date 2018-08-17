import java.util.*;
import java.lang.*;
import java.io.*;

public class BinaryShift {
    Scanner reader = new Scanner(System.in);
    public static void main(String args[]) throws java.lang.Exception{
        int n = reader.nextInt();  
        int pos = reader.nextInt();
        int shift = n>>pos;
        System.out.println(shift);
        System.out.println(Integer.toBinaryString(shift));
        if (Integer.toBinaryString(shift)[shift.length()-1] == "1")
            System.out.println("Yes");
        else
            System.out.println("No");       
    }
}