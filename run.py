import file_reader as fr
import plotter

model = fr.load_model("setups/setup_project.yaml")
model.solve()
solved_model = model.return_solved_model(scale=500)

print("Mass Efficiency: " + str(9000/model.find_mass()))

plotter.plot_model_setup(model)
plotter.plot_model_output(model, solved_model)