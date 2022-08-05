import numpy as np
from FeatureCloud.app.engine.app import app_state, AppState, Role, SMPCOperation
from tutorials.communicate import States


@app_state(name=States.initial.value)
class InitialState(AppState):
    def register(self):
        self.register_transition(States.broadcaster.value, Role.COORDINATOR)
        self.register_transition(States.waiter.value, Role.PARTICIPANT)

    def run(self):
        if self.is_coordinator:
            return States.broadcaster.value
        return States.waiter.value


@app_state(name=States.broadcaster.value, role=Role.COORDINATOR)
class BroadcasterState(AppState):
    def register(self):
        self.register_transition(States.sender.value, Role.COORDINATOR)

    def run(self):
        data = np.random.random((len(self.clients), 100, 10)).tolist()
        self.broadcast_data(data, send_to_self=False)
        ind = my_share(self.clients, self.id)
        self.store('data', data[ind])
        self.log('Initial data is broadcasted')
        return States.sender.value


@app_state(name=States.waiter.value, role=Role.PARTICIPANT)
class WaiterState(AppState):
    def register(self):
        self.register_transition(States.sender.value, Role.PARTICIPANT)

    def run(self):
        data = self.await_data()
        ind = my_share(self.clients, self.id)
        data = data[ind]
        self.log(f"Data is received. Data shape: {np.shape(data)}")
        self.store('data', data)
        return States.sender.value


@app_state(name=States.sender.value)
class SenderState(AppState):
    def register(self):
        self.register_transition(States.aggregator.value, Role.COORDINATOR)
        self.register_transition(States.terminal.value, Role.PARTICIPANT)

    def run(self):
        data = self.load('data')
        self.send_data_to_coordinator(data)
        self.log('Data is sent to the coordinator!')
        if self.is_coordinator:
            return States.aggregator.value
        return States.terminal.value


@app_state(name=States.aggregator.value, role=Role.COORDINATOR)
class AggregatorState(AppState):
    def register(self):
        self.register_transition(States.terminal.value, Role.COORDINATOR)

    def run(self):
        data = self.aggregate_data(operation=SMPCOperation.ADD)
        # data = self.gather_data()
        self.log(f"Data is aggregated: {np.shape(data)}")
        self.log(f"Data is aggregated: {data}")
        return States.terminal.value


def my_share(clients, id):
    for ind, c in enumerate(clients):
        if c == id:
            return ind
