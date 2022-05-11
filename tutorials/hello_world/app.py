from FeatureCloud.app.engine.app import app_state, AppState


@app_state(name='initial')
class InitialState(AppState):
    def register(self):
        self.register_transition('terminal')

    def run(self):
        self.log('Hello World!')
        return 'terminal'
