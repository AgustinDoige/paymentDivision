# Py-ment Division 

This is a short *console based* **Python program** that asks for a list of people and what they bought *(nothing is an option)* with the price (at, for example, a get-together).  
It also allowes for the input of exceptions, like if for any reason some person should be excempted of paying their share of a specific item (or a subset of purchases),
Calculates the specific amount each person should pay to who, and prints it into the screen.

#### Property:  
One property this algorithm has is that it minimizes(*) the amount of diferent payments the whole group will end up doing.

##### For example:  
###### *Scenario A:*
- p1 pays $40 to p3
- p1 pays $40 to p4
- p2 pays $40 to p3
- p2 pays $40 to p4
###### *Scenario B:*
- p1 pays $80 to p3
- p2 pays $80 to p4

While both scenarios are *equal* in the sense that the debts of everyone are the same, the algorithm would favor *Scenario B* that has a solution with less individual payments.  
###### (*) I think

### Idea: Calixto
### Code: Agustin Marcelo Dominguez (ADoige)
##### Sepember 2019

# Example Use

    Enter the names of every participant, one below the other:
    (Make 'end' the last entry)  

    >> person1
    >> person2
    >> person3
    >> end


    Enter what each person bought and it's price as a plain number     (without'$', decimals are allowed)
    Enter 'end' if the person mentioned didn't buy anything or as the last entry of each person
     Person1 bought: ('end' to terminate purchases of Person1)
    >> item1 200
    >> item2 34.3
    >> end
     Person2 bought: ('end' to terminate purchases of Person2)
    >> end
     Person3 bought: ('end' to terminate purchases of Person3)
    >> item3 156.2
    >> end
    Did everyone consume everything? (y/n): n
            Did Person1 not consume something? (y/n): n
            Did Person2 not consume something? (y/n): y
    'end' to terminate Person2 exceptions before
                    Did Person2 avoided consuming item1?     (y/n/end): y
                    Did Person2 avoided consuming item2?     (y/n/end): end
            Did Person3 not consume something? (y/n): n
    --> Person2 should pay $63.5 to Person1.
    --> Person3 should pay $7.299999999999997 to Person1.
