                                                                  
## A* Algorithm
### Why A*?                                                   
                                                                        
A* was chosen as the solver because it is both optimal (always finds the
shortest path) and efficient (explores fewer cells than a naive search
by using a heuristic).                                                  
                                                            
### How it works                                                          

A* assigns each cell a priority score:

$f(n) = g(n) + h(n)$
                                                                          
$g(n)$ — number of steps from the entry to cell n
$h(n)$ — estimated distance from n to the exit (heuristic)              
                                                                          
By always expanding the cell with the lowest f(n) first, A* focuses the search toward the exit instead of exploring in all directions equally.  
                                                         
Choosing the right heuristic                                            
   
The heuristic h(n) must match the movement rules of the map.            
                                                            
On a free map where diagonal movement is allowed, Euclidean distance is appropriate:                                              
$h(n) = √(dx² + dy²)$                                               
                                                          
In a maze, however, movement is restricted to four cardinal directions (N, E, S, W) — no diagonal steps are possible. Manhattan distance fits  
this constraint exactly:                                                
$h(n) = |dx| + |dy|$                                               
                                                                        
Using Manhattan distance here ensures the heuristic is admissible — it never overestimates the actual number of steps — which guarantees A* always finds the shortest path.

# State Machine                                                                         
### Overview                                                  

User interactions are managed by a generic state machine (StateMachine[S, E, C]). It separates what state the program is in from what to do when an event occurs, making the logic easy to extend.       
                                                            
At its core, the state machine is a lookup table mapping (state, event) pairs to (next state, action). This pattern is widely used beyond games and CLIs — payment processing systems, for example, use the same approach to manage order lifecycles (e.g. pending → authorized → captured → refunded).

States and transitions

GENERATE --[s]--> SOLVE --[S]--> SAVE
    ^               |               |
    └───────────────┴──────[g]──────┘
                                                           
### Design

Transitions are registered with a decorator, keeping the definition and
the action together:

@sm.transition(MazeState.GENERATE, Event.SHOW_SOLUTION, MazeState.SOLVE)
def do_solve(ctx: MazeContext) -> None:                                 
    ctx.maze_generator.solve(ctx.config.algorithm)
    ctx.maze_generator.display()                

reffered source : 
[![The State Pattern in Python](https://img.youtube.com/vi/OeirQdzYdnc/0.jpg)](https://www.youtube.com/watch?v=OeirQdzYdnc)
