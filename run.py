import file_reader as fr
import plotter

linespace = "-------------"

print(linespace)
print("Loading Model")
model = fr.load_model("setups/setup_project.yaml")
print("Load Complete")

print(linespace)
print("Solving model")
model.solve()
solved_model = model.return_solved_model(scale=500)
print("Solving complete")

print(linespace)
print("Mass Efficiency: " + str(9000/model.find_mass()))

plotter.console_output_displacements(model)

plotter.plot_model_setup(model)
plotter.plot_model_output(model, solved_model)