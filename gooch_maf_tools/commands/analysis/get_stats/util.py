import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector


def check_r_packages(packagenames: list):
	results = dict()
	for package in packagenames:
		results[package] = rpackages.isinstalled(package)
	return results


def check_and_install_R_dependency(library_name: str):
	required_r_packages = list([library_name])
	required_r_packages_install_status = check_r_packages(required_r_packages)
	need_to_install_r_packages = list()
	for package in required_r_packages_install_status:
		if not required_r_packages_install_status[package]:
			need_to_install_r_packages.append(package)
	if len(need_to_install_r_packages) > 0:
		utils = rpackages.importr('utils')
		utils.chooseCRANmirror(ind=1)
		utils.install_packages(StrVector(need_to_install_r_packages))