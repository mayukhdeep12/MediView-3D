# State Files

mediview-3d state files are a great way to save your scene and data to either be used later, or for distributing to collaborators and other users. These files store all of the information you need to restore the state of mediview-3d: your data, annotations, camera positions, background colors, colormaps, and more.

State files can be saved by clicking on "Disk" icon in the top of the toolbar. This button will generate a `*.mediview-3d.zip` file that can then be re-opened in mediview-3d at any time.

When saving mediview-3d state, your data is saved along with the application state. This way, when you send a state file to a collaborator, they too can open the state file and load the previously saved data. However, this means that your state file will be as large as your dataset(s) and may contain patient identifying information. Please follow your institutes HIPAA, IRB and other regulatory and confidentiality requirements.

State files are loaded by clicking on the "Folder" icon immediately below the save-state Disk icon. This will bring up a file browser for you to select and load your state file.

TIP: State files are a great way for developers to transfer data into / out of mediview-3d for integration with other systems. For example, they can be used to integrate mediview-3d with access control systems, to streamline workflows, or to ingest results from AI systems.
