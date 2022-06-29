import res.templates as templates_folder
from pathlib import Path
from importlib import resources

def get_templates_path() -> Path:
	with resources.path(templates_folder,'iapp.pdb') as structure_file:
		return structure_file.parent