#!/usr/bin/env python  

import sys, json, copy, os, gi

gi.require_version('Gtk', '3.0')  
from gi.repository import GLib, Gio, Gtk  

MENU_XML="""  
<?xml version="1.0" encoding="UTF-8"?>  
<interface>  
  <menu id="app-menu">  
    <section>  
      <item>  
        <attribute name="action">app.about</attribute>  
        <attribute name="label" translatable="yes">_About</attribute>  
      </item>  
      <item>  
        <attribute name="action">app.quit</attribute>  
        <attribute name="label" translatable="yes">_Quit</attribute>  
        <attribute name="accel">&lt;Primary&gt;q</attribute>  
    </item>  
    </section>  
  </menu>  
</interface>  
"""  

class ListBoxRowWithData(Gtk.ListBoxRow):  
    def __init__(self, data):  
        super(Gtk.ListBoxRow, self).__init__()  
        self.data = data  
        self.add(Gtk.Label(data))

class Dialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add Team", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Team number:")
        self.entry = Gtk.Entry()

        box = self.get_content_area()
        box.add(label)
        box.add(self.entry)
        self.show_all()

class AppWindow(Gtk.ApplicationWindow):  

    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        #Gtk.ApplicationWindow.__init__(self, title="Ursa Major Scouting")  
        self.set_default_size(800, 570)  

        self.hb = Gtk.HeaderBar()  
        self.hb.set_show_close_button(True)  
        self.hb.props.title = "Ursa Major Scouting"  
        self.set_titlebar(self.hb)   

        self.newbutton = Gtk.Button()  
        icon = Gio.ThemedIcon(name="document-new-symbolic")  
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON) 
        self.newbutton.add(image)  
        self.hb.pack_start(self.newbutton)  

        #button = Gtk.Button()  
        #icon = Gio.ThemedIcon(name="preferences-system-symbolic")  
        #image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)  
        #button.add(image)  
        #self.hb.pack_end(button)  

        self.view = Gtk.Paned()  
        self.add(self.view)  

        box_outer1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)  
        self.view.add(box_outer1)  

        self.teamslist = Gtk.ListBox()  
        self.teamslist.set_selection_mode(Gtk.SelectionMode.BROWSE)  
        self.teamslist.connect("row-selected", self.sidebarselected)  
        box_outer1.pack_start(self.teamslist, True, True, 0)  

        self.view.add1(box_outer1)  

        teamnumber = "template"

        self.notebook = Gtk.Notebook()  


        self.page1 = Gtk.ScrolledWindow()  
        self.page1.set_vexpand(True)
        self.page1box = Gtk.Box()
        self.page1box.set_border_width(10)  
        self.page1.add(self.page1box)


        self.standlistbox = Gtk.ListBox()  
        self.standlistbox.set_selection_mode(Gtk.SelectionMode.NONE)  
        self.page1box.pack_start(self.standlistbox, True, True, 0)  

        with open("Teams/" + teamnumber + ".json", 'r') as f:
            data = json.load(f)

        self.listboxrows = list()

        for category in data["Stand"]:
            row = Gtk.ListBoxRow()  
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)  
            row.add(hbox)  
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  
            hbox.pack_start(vbox, True, True, 0)  

            label1 = Gtk.Label("", xalign=0)  
            label1.set_markup("<big><b>" + category + "</b></big>")
            vbox.pack_start(label1, True, True, 0)  

            self.standlistbox.add(row)

            for item in data["Stand"][category]:
                row = Gtk.ListBoxRow()  
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)  
                row.add(hbox)  
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  
                hbox.pack_start(vbox, True, True, 0)  

                label1 = Gtk.Label(item, xalign=0)  
                vbox.pack_start(label1, True, True, 0)  

                value = Gtk.Entry()
                value.props.valign = Gtk.Align.CENTER  
                value.set_text(data["Stand"][category][item])
                value.connect("key-release-event", app.on_save)  
                hbox.pack_start(value, False, True, 0)  

                self.standlistbox.add(row)
                self.listboxrows.append(value)


        self.notebook.append_page(self.page1, Gtk.Label('Stand Scouting'))  


        self.page2 = Gtk.ScrolledWindow()  
        self.page2.set_vexpand(True)
        self.page2box = Gtk.Box()
        self.page2box.set_border_width(10)  
        self.page2.add(self.page2box)


        self.pitlistbox = Gtk.ListBox()  
        self.pitlistbox.set_selection_mode(Gtk.SelectionMode.NONE)  
        self.page2box.pack_start(self.pitlistbox, True, True, 0)  

        for item in data["Pit"]:
            row = Gtk.ListBoxRow()  
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)  
            row.add(hbox)  
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  
            hbox.pack_start(vbox, True, True, 0)  

            label1 = Gtk.Label(item, xalign=0)  
            vbox.pack_start(label1, True, True, 0)  

            value = Gtk.Entry()  
            value.props.valign = Gtk.Align.CENTER  
            value.set_text(data["Pit"][item])
            hbox.pack_start(value, False, True, 0)  

            self.pitlistbox.add(row)
            self.listboxrows.append(value)


        self.notebook.append_page(self.page2, Gtk.Label('Pit Scouting'))  
        self.view.add2(self.notebook) 
        self.newbutton.connect("clicked", self.newTeam)  

        dirListing = os.listdir("Teams")   
        editFiles = []
        for item in dirListing:
            if ".json" in item and item != "template.json":
                self.openteam(item.replace(".json", ""))

    def openteam(self, teamnumber):
        print("Opening " + teamnumber)

        if(os.path.exists("Teams/" + teamnumber + ".json")):
            path = teamnumber + ".json"
        else:
            path = "template.json"

        row = Gtk.ListBoxRow()  
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)  
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  
        hbox.pack_start(vbox, True, True, 0)  

        label1 = Gtk.Label(teamnumber, xalign=0)  
        row.add(label1)  
        vbox.pack_start(label1, True, True, 0)
        
        row.show_all()  

        self.teamslist.add(row) 

        self.teamslist.select_row(row)

    def newTeam(self, widget):
        dialog = Dialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:

            self.openteam(dialog.entry.get_text())

        dialog.destroy()

    def sidebarselected(self, widget, something):
        teamnumber = self.teamslist.get_selected_row().get_children()[0].get_text()

        if(os.path.exists("Teams/" + teamnumber + ".json")):
            path = teamnumber + ".json"
        else:
            path = "template.json"
            
        self.hb.props.title = teamnumber


        with open("Teams/" + path, 'r') as f:
            data = json.load(f)

        k = 0

        for category in data["Stand"]:

            for item in data["Stand"][category]:

                self.listboxrows[k].set_text(data["Stand"][category][item])
                k = k + 1

        for item in data["Pit"]:
            self.listboxrows[k].set_text(data["Pit"][item])
            k = k + 1

        print(app.saved)

    def changeSavedStatus(self, widget, ev, data=None):
        app.saved = False

class Application(Gtk.Application):  

    def __init__(self, *args, **kwargs):  
        super().__init__(*args, application_id="org.hammondursamajor.Scouting",  
                         **kwargs)  
        self.window = None  
        self.saved = True

    def do_startup(self):  
        Gtk.Application.do_startup(self)  
          
        #settings = Gtk.Settings.get_default()  
        #settings.set_property("gtk-application-prefer-dark-theme", True)  

        action = Gio.SimpleAction.new("save", None)  
        action.connect("activate", self.on_save)  
        self.add_action(action)  

        action = Gio.SimpleAction.new("about", None)  
        action.connect("activate", self.on_about)  
        self.add_action(action)  

        action = Gio.SimpleAction.new("quit", None)  
        action.connect("activate", self.on_quit)  
        self.add_action(action)  

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)  
        self.set_app_menu(builder.get_object("app-menu"))  

    def do_activate(self):  
        # We only allow a single window and raise any existing ones  
        if not self.window:  
            # Windows are associated with the application  
            # when the last one is closed the application shuts down  
            self.window = AppWindow(application=self, title="Ursa Major Scouting")  


        self.window.set_icon_from_file('/home/james/UrsaMajorScouting/0.png')  
        self.window.show_all()  

    def on_about(self, action, param):  
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)  
        about_dialog.present()  

    def on_save(self, action, param):  
        
        with open('Teams/template.json', 'r') as f:
            olddata = json.load(f)

        data = copy.copy(olddata)

        savedata = list()
        children = self.window.standlistbox.get_children()
        for child in children:
            if child is not None:
                ch2 = child.get_children()
                for child2 in ch2:
                    ch3 = child2.get_children()
                    for child3 in ch3:
                        if isinstance(child3, Gtk.Entry):
                            savedata.append(child3.get_text())
        
        i = 0
        j = 0
        for category in olddata["Stand"]:
            keys = list()
            for key in olddata["Stand"][category]:
                keys.append(key)
            
            i = 0
            for item in olddata["Stand"][category]:
                keyname = keys[i]
                data["Stand"][category][keyname] = savedata[j]
                i = i+1
                j = j+1



        savedata = list()
        children = self.window.pitlistbox.get_children()
        for child in children:
            if child is not None:
                ch2 = child.get_children()
                for child2 in ch2:
                    ch3 = child2.get_children()
                    for child3 in ch3:
                        if isinstance(child3, Gtk.Entry):
                            savedata.append(child3.get_text())
        
        keys = list()
        for key in olddata["Pit"]:
            keys.append(key)
        
        i = 0
        j = 0
        for item in olddata["Pit"]:
            keyname = keys[i]
            data["Pit"][keyname] = savedata[j]
            i = i+1
            j = j+1
        
        filename = self.window.teamslist.get_selected_row().get_children()[0].get_text()
        
        with open("Teams/" + filename + ".json", 'w') as f:
            json.dump(data, f)

        self.saved = True


        #dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
        #    Gtk.ButtonsType.OK, "File saved")
        #dialog.format_secondary_text(
        #    "Information for team " + filename + " has been saved to " + filename + ".json")
        #dialog.run()

        #dialog.destroy()

        


    def on_quit(self, action, param):  
        self.quit()  

if __name__ == "__main__":  
    app = Application()  
    app.run(sys.argv)  


#team = Team(2849, "Ursa Major")  

#win = MainWindow()  
#win.connect("delete-event", Gtk.main_quit)  
#win.show_all()  
#Gtk.main()  
