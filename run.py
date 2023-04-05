import file_reader as fr
import plotter
import math

linespace = "-------------"

print(linespace)
print("Loading Model")
model = fr.load_model("setups/setup_project3v3_matched_names.yaml")
print("Load Complete")

print(linespace)
print("Solving Model")
model.solve()
model.find_nodal_displacements()
print("Solving Complete")

print(linespace)
print("Starting Post Proccesing")
model.post_procces()
print("Post Proccesing Complete")

print(linespace)
print("Mass Efficiency: " + str(9000/model.find_mass()))

plotter.console_output_displacements(model)
plotter.console_output_stresses(model)

plotter.plot_model_setup(model)
plotter.plot_model_displacements(model, scale=10)
plotter.plot_model_displacements(model, scale=1, undeformed=False, stress=True)