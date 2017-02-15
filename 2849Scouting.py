#!/usr/bin/env python  

import sys
import json
from pprint import pprint

import gi  
gi.require_version('Gtk', '3.0')  
from gi.repository import GLib, Gio, Gtk  

MENU_XML="""  
<?xml version="1.0" encoding="UTF-8"?>  
<interface>  
  <menu id="app-menu">  
    <section>  
      <item>  
        <attribute name="action">app.save</attribute>  
        <attribute name="label" translatable="yes">_Save</attribute>  
      </item>  
      <item>  
        <attribute name="action">app.reload</attribute>  
        <attribute name="label" translatable="yes">_Reload</attribute>  
    </item>  
    </section>  
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

class Team:  
    def __init__(self, number, name):  
        self.number = number  
        self.name = name  

    def __str__(self):  
        return "+-----+ " + self.name + " +-----+" + "\n" + "Number: " + str(self.number)  





class ListBoxRowWithData(Gtk.ListBoxRow):  
    def __init__(self, data):  
        super(Gtk.ListBoxRow, self).__init__()  
        self.data = data  
        self.add(Gtk.Label(data))  

class SaveDialog(Gtk.Dialog):  

    def __init__(self, parent):  
        Gtk.Dialog.__init__(self, "Save", parent, 0,  
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,  
             Gtk.STOCK_OK, Gtk.ResponseType.OK))  

        self.set_default_size(150, 100)  

        label = Gtk.Label("Saving file...")  

        box = self.get_content_area()  
        box.add(label)  
        self.show_all()  

class AppWindow(Gtk.ApplicationWindow):  

    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        #Gtk.ApplicationWindow.__init__(self, title="Ursa Major Scouting")  
        self.set_default_size(800, 570)  

        hb = Gtk.HeaderBar()  
        hb.set_show_close_button(True)  
        hb.props.title = "Ursa Major Scouting"  
        self.set_titlebar(hb)  

        button = Gtk.Button()  
        icon = Gio.ThemedIcon(name="document-save-symbolic")  
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)  
        button.connect("clicked", app.on_save)  
        button.add(image)  
        hb.pack_start(button)  

        button = Gtk.Button()  
        icon = Gio.ThemedIcon(name="preferences-system-symbolic")  
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)  
        button.add(image)  
        hb.pack_end(button)  

        self.view = Gtk.Paned()  
        self.add(self.view)  

        box_outer1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)  
        self.view.add(box_outer1)  

        teamslist = Gtk.ListBox()  
        teamslist.set_selection_mode(Gtk.SelectionMode.BROWSE)  
        box_outer1.pack_start(teamslist, True, True, 0)  

        row = Gtk.ListBoxRow()  
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)  
        row.add(hbox)  
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  
        hbox.pack_start(vbox, True, True, 0)  

        label1 = Gtk.Label("Ursa Major - 2849", xalign=0)  
        vbox.pack_start(label1, True, True, 0)  

        teamslist.add(row)  

        self.view.add1(box_outer1)  

        self.notebook = Gtk.Notebook()  

        self.page1 = Gtk.ScrolledWindow()  
        self.page1.set_vexpand(True)
        self.page1box = Gtk.Box()
        self.page1box.set_border_width(10)  
        self.page1.add(self.page1box)


        listbox = Gtk.ListBox()  
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)  
        self.page1box.pack_start(listbox, True, True, 0)  

        with open('template.json', 'r') as f:
            data = json.load(f)

        for category in data["Stand"]:
            row = Gtk.ListBoxRow()  
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)  
            row.add(hbox)  
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  
            hbox.pack_start(vbox, True, True, 0)  

            label1 = Gtk.Label("", xalign=0)  
            label1.set_markup("<big><b>" + category + "</b></big>")
            vbox.pack_start(label1, True, True, 0)  

            listbox.add(row)

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
                hbox.pack_start(value, False, True, 0)  

                listbox.add(row)


        self.notebook.append_page(self.page1, Gtk.Label('Stand Scouting'))  


        self.page2 = Gtk.ScrolledWindow()  
        self.page2.set_vexpand(True)
        self.page2box = Gtk.Box()
        self.page2box.set_border_width(10)  
        self.page2.add(self.page2box)


        listbox = Gtk.ListBox()  
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)  
        self.page2box.pack_start(listbox, True, True, 0)  

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

            listbox.add(row)

        self.notebook.append_page(self.page2, Gtk.Label('Pit Scouting'))  
        self.view.add2(self.notebook)  

class Application(Gtk.Application):  

    def __init__(self, *args, **kwargs):  
        super().__init__(*args, application_id="org.hammondursamajor.Scouting",  
                         **kwargs)  
        self.window = None  

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

    def on_save(self, action):  
        dialog = SaveDialog(self.window)  
        response = dialog.run()  

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
