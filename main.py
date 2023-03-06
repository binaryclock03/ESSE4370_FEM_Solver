import file_reader as fr
import plotter

model = fr.load_model("setup_project.yaml")

model.solve()

print(model.row_tracker)
solved_model = model.return_solved_model(scale=500)

print(9000/model.find_mass())

plotter.plot_model(model)
plotter.plot_model2(model, solved_model)