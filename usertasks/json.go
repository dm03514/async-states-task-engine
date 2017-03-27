package usertasks

// import "github.com/dm03514/async-states-task-engine/task"

const (
	VERSION int = 1
	ACTION_TYPE_HTTP string = "http"
	ACTION_METHOD_POLL string = "poll"
)


type Action struct {
	Type string
	Instruction string
	Method string
}

type Event struct {
	Instructions []Action
	TransitionConditions []Action
	StartState string
	EndState string
}


type UserTask struct {
	Version string
	StartState string
	FinalState string
	MaxTimeout int
	Events []Event
}

// constructions and returns an instance of ITask built from the
// data defined by an end user.
// func (UserTask) ITask() task.ITask {}




