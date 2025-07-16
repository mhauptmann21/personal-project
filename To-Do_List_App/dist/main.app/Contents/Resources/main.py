from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from models import Task
from task_manager import load_tasks, save_tasks, get_next_id

class ToDoLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.tasks = load_tasks()

        # Inputs
        self.input_title = TextInput(hint_text="Task title", size_hint_y=0.1)
        self.add_widget(self.input_title)

        self.input_due = TextInput(hint_text="Due date (YYYY-MM-DD)", size_hint_y=0.1)
        self.add_widget(self.input_due)

        self.input_priority = Spinner(
            text='medium',
            values=('low', 'medium', 'high'),
            size_hint_y=0.1
        )
        self.add_widget(self.input_priority)

        add_btn = Button(text="Add Task", size_hint_y=0.1)
        add_btn.bind(on_press=self.add_task)
        self.add_widget(add_btn)

        # Scrollable Task List
        self.task_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))

        scroll = ScrollView(size_hint=(1, 0.6))
        scroll.add_widget(self.task_list)
        self.add_widget(scroll)

        self.refresh_tasks()

    def refresh_tasks(self):
        self.task_list.clear_widgets()
        for task in sorted(self.tasks, key=lambda t: (t.done, t.priority, t.due_date or "")):
            color = (0.5, 1, 0.5, 1) if task.done else (1, 1, 1, 1)
            btn = Button(
                text=f"{task.title} [{task.priority}] Due: {task.due_date or 'N/A'} {'✓' if task.done else ''}",
                size_hint_y=None,
                height=40,
                background_color=color
            )
            btn.bind(on_press=lambda b, t=task: self.toggle_done(t))
            btn.bind(on_release=lambda b, t=task: self.confirm_delete(t))
            self.task_list.add_widget(btn)

    def add_task(self, instance):
        title = self.input_title.text.strip()
        due = self.input_due.text.strip() or None
        priority = self.input_priority.text.strip().lower()

        if title:
            new_task = Task(
                id=get_next_id(self.tasks),
                title=title,
                priority=priority,
                due_date=due,
                done=False
            )
            self.tasks.append(new_task)
            self.input_title.text = ""
            self.input_due.text = ""
            self.input_priority.text = "medium"
            self.refresh_tasks()

    def toggle_done(self, task):
        task.done = not task.done
        self.refresh_tasks()

    def confirm_delete(self, task):
        content = BoxLayout(orientation='vertical')
        msg = Label(text=f"Delete task '{task.title}'?")
        btns = BoxLayout(size_hint_y=0.3)

        yes = Button(text="Yes")
        no = Button(text="No")

        btns.add_widget(yes)
        btns.add_widget(no)
        content.add_widget(msg)
        content.add_widget(btns)

        popup = Popup(title="Confirm Delete", content=content, size_hint=(0.8, 0.4))

        yes.bind(on_press=lambda x: self.delete_task(task, popup))
        no.bind(on_press=popup.dismiss)

        popup.open()

    def delete_task(self, task, popup):
        self.tasks = [t for t in self.tasks if t.id != task.id]
        popup.dismiss()
        self.refresh_tasks()

    def on_parent(self, widget, parent):
        if not parent:
            save_tasks(self.tasks)

class ToDoApp(App):
    def build(self):
        return ToDoLayout()

    def on_stop(self):
        save_tasks(self.root.tasks)

if __name__ == '__main__':
    ToDoApp().run()