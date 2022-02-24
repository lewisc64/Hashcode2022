class Contributor:

    def __init__(self, name):
        self.name = name
        self.skills = {}

    def set_skill(self, skill_name, level):
        self.skills[skill_name] = level

    def get_skill_level(self, skill_name):
        return self.skills[skill_name]

    def increment_skill(self, skill_name):
        self.skills[skill_name] += 1

    def __str__(self):
        return f"Contributor({self.name}, {self.skills})"

class Requirement:

    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.assignee = None

    def assign(self, contributor):
        self.assignee = contributor

    def contributor_can_do(self, contributor):
        return self.name in contributor.skills and contributor.skills[self.name] >= self.level

    def contributor_can_do_minus_one(self, contributor):
        if self.level <= 1:
            return True
        return self.name in contributor.skills and contributor.skills[self.name] == self.level - 1

    def __str__(self):
        return f"Requirement({self.name}, {self.level})"

class Project:
    
    def __init__(self, name, days_to_complete, score_awarded, best_before, contributors_required, requirements):
        self.name = name
        self.days_to_complete = days_to_complete
        self.score_awarded = score_awarded
        self.best_before = best_before
        self.contributors_required = contributors_required
        self.requirements = requirements
        self.chances = 3

    def make_them_learn(self):
        for requirement in self.requirements:
            if requirement.name not in requirement.assignee.skills:
                requirement.assignee.skills[requirement.name] = 1
            
            elif requirement.assignee.skills[requirement.name] <= requirement.level:
                requirement.assignee.skills[requirement.name] += 1

    def __str__(self):
        return f"Project({self.name}, {[str(x) for x in self.requirements]})"

def load_file(path):
    content = ""
    with open(path, "r") as file:
        content = file.read()

    lines = content.splitlines()

    num_contributors, num_projects = [int(x) for x in lines[0].split(" ")]

    nerd_squad = []
    projects = []

    i = 1
    for x in range(num_contributors):
        name, num_skills = lines[i].split(" ")

        contributor = Contributor(name)

        for y in range(int(num_skills)):
            i += 1
            skill_name, skill_level = lines[i].split(" ")
            contributor.set_skill(skill_name, int(skill_level))

        nerd_squad.append(contributor)
        i += 1

    for x in range(num_projects):
        name, data = lines[i].split(" ", 1)
        data = data.split(" ")
        
        days_to_complete = int(data[0])
        score_awarded = int(data[1])
        best_before = int(data[2])
        contributors_required = int(data[3])

        requirements = []

        for y in range(contributors_required):
            i += 1
            skill_name, level = lines[i].split(" ")
            requirements.append(Requirement(skill_name, int(level)))

        project = Project(name, days_to_complete, score_awarded, best_before, contributors_required, requirements)
        projects.append(project)
        i += 1

    return nerd_squad, projects

def process(squad, projects):
    
    done_projects = []
    projects.sort(key=lambda x: -max([y.level for y in x.requirements]))
    squad.sort(key=lambda x: sum(x.skills.values()))

    while len(projects) > 0:
        project = projects[0]

        #print("PROCESS PROJECT", project.name)
        
        fulfilled = True

        others = []
        
        for requirement in project.requirements:

            #print("  PROCESS REQ", requirement)

            for contributor in squad:
                if contributor in others:
                    continue
                if requirement.contributor_can_do_minus_one(contributor):
                    for other in others:
                        if requirement.contributor_can_do(other):
                            #print(f"    Assigning {contributor.name}, mentored!")
                            requirement.assign(contributor)
                            others.append(contributor)
                            break
                    else:
                        continue
                    break
            else:
                for contributor in squad:
                    if contributor in others:
                        continue
                    if requirement.contributor_can_do(contributor):
                        #print(f"    Assigning {contributor.name}, can do!")
                        requirement.assign(contributor)
                        others.append(contributor)
                        break
                else:
                    #print("    nobody can do this...")
                    fulfilled = False
                    break

        if fulfilled:
            #print(f"PROJECT {project.name} IS GOOD TO GO!")
            project.make_them_learn()
            projects.remove(project)
            done_projects.append(project)
        else:
            #print(f"PROJECT {project.name} IS REJECTED! TEAM SUCKS")
            for requirement in project.requirements:
                requirement.assignee = None

            if (project.chances == 0):
                #print("IT IS TOO OLD AND MUST DIE")
                projects.remove(project)
            else:
                #print("DEFERRED!!")
                project.chances -= 1
                projects.remove(project)
                #projects.insert(i + 2, project)
                projects.append(project)
    return done_projects

def process_file(path):
    print(f"processing {path}...")
    output_path = path.replace(".in.", ".out.")
    
    squad, projects = load_file(path)
    done_projects = process(squad, projects)

    content = f"{len(done_projects)}"
    for project in done_projects:
        names = " ".join([x.assignee.name for x in project.requirements])
        content += f"\n{project.name}\n{names}"
    
    with open(output_path, "w") as file:
        file.write(content)
    print(f"done, written to {output_path}")

if __name__ == "__main__":
    process_file("data/a_an_example.in.txt")
    process_file("data/b_better_start_small.in.txt")
    process_file("data/c_collaboration.in.txt")
    process_file("data/d_dense_schedule.in.txt")
    process_file("data/e_exceptional_skills.in.txt")
    process_file("data/f_find_great_mentors.in.txt")
