from force_bdss import *

wf=Workflow()
wf.set_mco(Dakota())
wf.set_datasources([
    ViscositySimulator(),
    CostExtractor(),
])
wf.objectives([
    Objective(),
    Objective()
    ])


wf.set_parameters({
    "material_1": {
        CUBA.FORMULA: "H2O",
        CUBA.CONCENTRATION: Range(0, 100)
    },
    "material_2": {
        CUBA.FORMULA: "glycol",
        CUBA.CONCENTRATION: Formula("material_1",
            lambda material_1: 100 - material_1[CUBA.CONCENTRATION])
    }
})

wf.set_result_callback(callback)

# constraints vs computed value
# e.g. constraint = value from 0 to 100
# computed value = 100 - other value
# TODO: Study dakota better to understand how it works and what kind of
# interface it expects

pareto_front = wf.execute()

plot(pareto_front)

