import pathlib
import os
import tkinter.messagebox
from datetime import datetime
from idlelib.tooltip import Hovertip
from inspect import currentframe, getframeinfo
from pprint import pprint
from tkinter import *
from tkinter.ttk import *

import github

ENV_GITHUB_TOKEN = 'GITHUB_TOKEN'
repo_columns = ('name',  'private', 'size',
                'clone_url',   'language', 'description', 'created_at', 'pushed_at')


def get_github_token():
    if ENV_GITHUB_TOKEN in os.environ:
        return os.environ[ENV_GITHUB_TOKEN]
    else:
        return None


def handler_create_repository():
    try:
        GITHUB_TOKEN = get_github_token()
        repository_name = entryRepoName.get().strip()
        repository_description = entryRepoDescription.get().strip()
        if not repository_name:
            # https://docs.python.org/3/library/tkinter.messagebox.html
            tkinter.messagebox.showwarning(
                "Missing input", "Repository name is mandatory")
            entryRepoName.focus()
            return
        print(
            f"Creating Github repository '{repository_name}' with description '{repository_description}'")
        result = github.create_repo(GITHUB_TOKEN, repository_name,
                                    repository_description)
        txt_result.config(state=NORMAL)
        txt_result.delete("1.0", END)
        txt_result.insert("1.0", result)
        txt_result.config(state=DISABLED)
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror("Error creating repository", e.args)


def populate_repository_treeview():
    repos = []
    for repo in github.list_repositories(get_github_token()):
        repos.append(repo)

    # Last pushed repos should be displayed first
    repos.sort(key=lambda r: r['pushed_at'], reverse=True)

    for repo in repos:
        tree_repos.insert(parent='',
                          index=END,
                          values=(repo[repo_columns[0]],
                                  repo[repo_columns[1]],
                                  repo[repo_columns[2]],  # size
                                  repo[repo_columns[3]],
                                  repo[repo_columns[4]],
                                  repo[repo_columns[5]],
                                  repo[repo_columns[6]],
                                  repo[repo_columns[7]]))
    return len(repos)


def handler_notebook_tab_changed(ev: Event):
    notebook: Notebook = ev.widget
    tab_index = notebook.index("current")
    tab_text: str = notebook.tab(notebook.select(), "text")
    print("Selected notebook tab:", f"{tab_index=}", f"{tab_text=}")
    if tab_text.startswith("Create"):
        if (get_github_token()):
            variable_statusbar.set(
                f"Environment variable {ENV_GITHUB_TOKEN} found.")
        else:
            variable_statusbar.set(
                f"WARNING: Environment variable {ENV_GITHUB_TOKEN} not found.")
    elif tab_text.startswith("List"):
        variable_statusbar.set("Fetching repositories...")
        window.update()
        num_repos = populate_repository_treeview()
        variable_statusbar.set(f"{num_repos} Github repositories")


window = Tk()
window.iconbitmap(pathlib.Path(__file__).parent / 'github.ico')
window.minsize(400, 400)
window.title("Github Repository Manager")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)


def copy_to_clipboard(widget: Tk, text: str):
    # widget.withdraw()
    widget.clipboard_clear()
    widget.clipboard_append(text)
    widget.update()  # now it stays on the clipboard after the window is closed


myTip = Hovertip(window, 'This is \na multiline tooltip.', hover_delay=1000)

aMenu = Menu(window, tearoff=0)
# aMenu.add_command(label='Delete', command=None)
aMenu.add_command(label='Copy URL',
                  command=lambda:
                  # print(tree_repos.set(tree_repos.focus()))
                  copy_to_clipboard(window, tree_repos.set(
                      tree_repos.selection()[0])['clone_url'])
                  )

variable_statusbar = StringVar()


# https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Notebook
notebook = Notebook(window)
notebook.grid(row=0, column=0, sticky=(N, S, E, W))
notebook.bind('<<NotebookTabChanged>>', handler_notebook_tab_changed)

# STATUS BAR
Label(window, textvariable=variable_statusbar).grid(
    row=1, column=0)

# CREATE A NEW REPOSITORY
frame1 = Frame(window, padding=10)
frame1.rowconfigure([0, 1, 2, 3], pad=10)
frame1.rowconfigure(3, weight=1)
frame1.columnconfigure(0, pad=10)
frame1.columnconfigure(1, pad=10, weight=1)

notebook.add(frame1, text="Create a new repository")

Label(frame1, text="Repository name: ").grid(row=0, column=0, sticky='e')
entryRepoName = Entry(frame1)
entryRepoName.grid(row=0, column=1, sticky='we')
entryRepoName.focus()

Label(frame1, text="Repository description: ").grid(
    row=1, column=0, sticky='e')
entryRepoDescription = Entry(frame1, width=100)
entryRepoDescription.grid(row=1, column=1, sticky='we')

btnCreate = Button(frame1,
                   text="Create repository on Github",
                   command=handler_create_repository)
btnCreate.grid(row=2, columnspan=2)

txt_result = Text(frame1,
                  exportselection=True,
                  bg="#EEE",
                  selectbackground='#00F',
                  selectforeground='#fff')
txt_result.grid(row=3, columnspan=2, sticky='nswe')
txt_result.config(state=DISABLED)


# LIST ALL REPOSITORIES
frame2 = Frame(window, padding=10)
frame2.rowconfigure(0, pad=10, weight=1)
frame2.columnconfigure(0, pad=10, weight=1)

notebook.add(frame2, text="List all repositories")


def handler_tree_repos_right_click(event):
    iid = tree_repos.identify_row(event.y)
    if iid:
        # mouse pointer over item
        tree_repos.selection_set(iid)

        # frameinfo = getframeinfo(currentframe())
        # print(frameinfo.filename, frameinfo.lineno)
        # pprint(tree_repos.set(iid))

        aMenu.post(event.x_root, event.y_root)


tree_repos = Treeview(frame2,
                      show='headings',
                      selectmode='browse',
                      height=18)
tree_repos.bind("<Button-3>", handler_tree_repos_right_click)


tree_repos['columns'] = repo_columns
tree_repos.column('private', width=40)
tree_repos.column('size', anchor=E, width=40, minwidth=25)
tree_repos.column('language', width=50)
# tree.column('zone_id',  width=110, minwidth=100)
# tree.column('#0', width=120, minwidth=25)
# tree.column('#0', width=120, minwidth=25)


def handler_sort_treeview(tv, col, reverse, conversion_func):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key=lambda t: conversion_func(t[0]), reverse=reverse)

    # rearrange items in sorted positions
    for index, (_, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda:
               handler_sort_treeview(tv, col, not reverse, conversion_func))


def create_sort_handler(col, conversion_func=str):
    def sort():
        handler_sort_treeview(tree_repos, col, False, conversion_func)
    return sort


tree_repos.heading('name', text='Name', anchor=W,
                   command=create_sort_handler('name'))
tree_repos.heading('private', text='Private?', anchor=W)
tree_repos.heading('clone_url', text='URL', anchor=W)
tree_repos.heading('description', text='Description', anchor=W)
tree_repos.heading('size', text='Size', anchor=E,
                   command=create_sort_handler('size', int))
tree_repos.heading('language', text='Language', anchor=W,
                   command=create_sort_handler('language'))
tree_repos.heading('created_at', text='Created',
                   anchor=W, command=create_sort_handler('created_at'))
tree_repos.heading('pushed_at', text='Pushed', anchor=W,
                   command=create_sort_handler('pushed_at'))
# tree_repos.tag_configure('zone', background='#0E0')


tree_repos.grid(row=0, column=0, sticky='nswe')

scrollbar = Scrollbar(
    frame2,
    orient='vertical',
    command=tree_repos.yview


)
scrollbar.grid(row=0, column=1, sticky='ns')

tree_repos.configure(yscrollcommand=scrollbar.set)

window.mainloop()
