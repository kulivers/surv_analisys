from lifelines import CoxPHFitter

from UmdbHelper import UmdbHelper
from UmdbRepository import UmdbRepository

helper = UmdbHelper()
repo = UmdbRepository()

common_path = repo.getMostCommonDiagnosesPaths()[0]
records = repo.getPatientsByDiagnosysPath(common_path)

cph = CoxPHFitter()

status_duration_dict = helper.getStatusAndLiveDurationsOfPatients(records)

df = helper.formatDf(records,)
# cph.fit(df=bc_df, duration_col='time', event_col='status', formula='sex')

# cph.print_summary()
