classDiagram
    User "1" --> "0..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler "1" --> "0..*" Task : schedules

    class User {
        +String name
        +List~Pet~ pets
        +addPet(pet: Pet)
        +removePet(name: String)
        +viewPets() List~Pet~
    }

    class Pet {
        +String name
        +String species
        +int age
        +List~Task~ tasks
        +addTask(task: Task)
        +removeTask(name: String)
        +viewTasks() List~Task~
    }

    class Task {
        +String name
        +String priority
        +int duration
        +setDuration(minutes: int)
        +setPriority(level: String)
    }

    class Scheduler {
        +List~Task~ tasks
        +int timeAvailable
        +makeSchedule() List~Task~
        +sortByPriority() List~Task~
        +fitTimes() List~Task~
        +explainFit() String
    }