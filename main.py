from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.utils import platform
from plyer import filechooser
import Fruits

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])

Builder.load_file('interface.kv')

class MyLayout(Widget):

    selection = ObjectProperty()

    def choose(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = selection[0]

    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        App.get_running_app().root.ids.my_image.source = self.selection

class HandPoseApp(App):

    def build(self):
        return(MyLayout())

    def classify_image(self):
        img_path = self.root.ids["my_image"].source

        img_features = Fruits.extract_features(img_path)

        predicted_class = Fruits.predict_output("weights.npy", img_features, activation="sigmoid")

        self.root.ids["label"].text = "Predicted Class : " + predicted_class

#firstApp = AwesomeApp(title="Fruits 360 Recognition")
#firstApp.run()

if __name__ == '__main__':
    HandPoseApp().run()
