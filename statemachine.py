from dataclasses import dataclass, field
from enum import Enum, auto, StrEnum
from typing import Callable, Iterable
from config import Config
from mazegen import MazeGenerator



type Action[C] = Callable[[C], None]


class InvalidTransition(Exception):
	pass

@dataclass
class MazeContext:
	maze_generator: MazeGenerator
	config: Config


class MazeState(Enum):
	GENERATE = auto()
	SOLVE = auto()
	SAVE = auto()

class Event(StrEnum):
	GENERATE = "g"
	SHOW_SOLUTION = "s"
	HIDE_SOLUTION = "h"
	SAVE = "S"
	QUIT = "q"
	COLORS = "c"


@dataclass
class StateMachine[S: Enum, E: Enum, C]:
	transitions: dict[tuple[S, E], tuple[S, Action[C]]] = field(
		default_factory=dict[tuple[S, E], tuple[S, Action[C]]]
	)

	def add_transition(
		self, from_state: S, event: E, to_state: S, func: Action[C]
	) -> None:
		self.transitions[(from_state, event)] = (to_state, func)
	
	def next_transition(self, state: S, event: E) -> tuple[S, Action[C]]:
		try:
			return self.transitions[(state, event)]
		except KeyError as e:
			raise InvalidTransition(f"Can not {event.name}"
									f" when {state.name}") from e
	
	def handle(self, ctx: C, state: S, event: E) -> S:
		next_state, action = self.next_transition(state, event)
		action(ctx)
		return next_state

	def transition(self, from_state: S | Iterable[S],
				event: E, to_state: S) -> Action:
		if not isinstance(from_state, Iterable):
			from_state = (from_state,)
		
		def decorator(func: Action[C]) -> Action[C]:
			for s in from_state:
				self.add_transition(s, event, to_state, func)
			return func
		return decorator
		
		
sm: StateMachine[MazeState, Event, MazeContext] = StateMachine()

@sm.transition(MazeState.GENERATE, Event.GENERATE, MazeState.GENERATE)
@sm.transition(MazeState.SOLVE, Event.GENERATE, MazeState.GENERATE)
@sm.transition(MazeState.SAVE, Event.GENERATE, MazeState.GENERATE)
def do_generate(ctx: MazeContext) -> None:
	ctx.maze_generator = MazeGenerator.from_config(ctx.config)
	ctx.maze_generator.generate(ctx.config.perfect, ctx.config.seed)
	ctx.maze_generator.display()
	print(f"Generated maze (seed: {ctx.maze_generator.seed})")
	print()
	print("[g]enerate | [s]olve | [q]uit | [c]olor")

@sm.transition(MazeState.GENERATE, Event.SHOW_SOLUTION, MazeState.SOLVE)
def do_solve(ctx: MazeContext) -> None:
    ctx.maze_generator.solve(ctx.config.algorithm)
    ctx.maze_generator.display()
    print(f"Solved maze (seed: {ctx.maze_generator.seed})")
    print()
    print("[g]enerate | [h]ide solution | [S]ave | [q]uit")

@sm.transition(MazeState.SOLVE, Event.SAVE, MazeState.SAVE)
def do_save(ctx: MazeContext) -> None:
    ctx.maze_generator.save(ctx.config.output_file)
    print(f"Generated maze (seed: {ctx.maze_generator.seed})")
    print()
    print("[g]enerate | [s]olve | [q]uit | [c]olor")

@sm.transition(MazeState.SOLVE, Event.HIDE_SOLUTION, MazeState.SOLVE)
def do_hide_solution(ctx: MazeContext) -> None:
    if not ctx.maze_generator.renderer.hide_solution():
        return
    ctx.maze_generator.display()

@sm.transition(MazeState.SOLVE, Event.SHOW_SOLUTION, MazeState.SOLVE)
def do_show_solution(ctx: MazeContext) -> None:
    if not ctx.maze_generator.renderer.show_solution():
        return
    ctx.maze_generator.display()

@sm.transition(MazeState.GENERATE, Event.COLORS, MazeState.GENERATE)
@sm.transition(MazeState.SOLVE, Event.COLORS, MazeState.SOLVE)
@sm.transition(MazeState.SAVE, Event.COLORS, MazeState.SAVE)
def do_colors(ctx: MazeContext) -> None:
    ctx.maze_generator.renderer.random_color(ctx.maze_generator.grid)
    ctx.maze_generator.display()