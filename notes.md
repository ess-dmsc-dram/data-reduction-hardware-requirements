# Hardware requirements for data reduction

## Assumptions

- Assume that the cluster is large, such that we do not need to take into account holes from a single job requiring a significant fraction of cores.
  The final result should probably be scaled by an appropriate fill factor, which DST/cluster admins should be able to provide based on past experience.

## Performance master equation

With a couple of approximations (which are probably minor for this purpose and compared to other sources of uncertainty) we can describe the time required to reduce a set of data with the following formula:

```
t = t_0 + (N_spec*t_spec + N_event*t_event)/N_core + N_event/bandwidth_max
```

Here:

- `N_spec` is the number of spectra in the workflow.
  Typically this is the number of pixels of the instrument, but it can be different, e.g., when data from pixels is split up, such as for event filtering or RRM.
- `N_event` is the total number of events that are being handled in the reduction workflow.
  This can include events from multiple files, e.g., for a sample run and a background run.
- `N_core` is the number of cores (MPI ranks) used in the reduction.
  We are not considering a hybrid threading+MPI approach (apart from a few specialized algorithms that are using threading internally).
- `t_0` is a constant time specific to the reduction workflow.
  It includes anything that does not depend and the number of spectra or number of events.
  Typically this includes small parts of the time spend in every algorithm, time for loading experiment logs from NeXus files, time for loading auxiliary files, and other overheads.
- `t_spec` is the (computed) time to run the workflow for a single spectra.
- `t_event` is the (computed) time to run the workflow for a single event.
- `bandwidth_max` is the number of events that can be loaded from the file system per second.

The rationale for this equation is as follows:

- For the vast majority of algorithms used in data reduction, all spectra are treated independently.
  Thus there is a linear term in `N_spec`, but no higher order terms, and there is perfect scaling with `N_core`.
- Events in Mantid are stored with their respective spectrum.
  Strictly speaking, we should thus include a term
  ```
  \sum_{i=1}^{N_spec} (N_{event,i} * t_{event,linear} + N_{event,i} log N_{event,i} * t_{event,NlogN} + ...),
  ```
  i.e., a different term for each spectrum, depending on the number of events in that spectrum, and non-linear term, such as for sorting events.
  However, events are usually spread over many spectra, so we can approximate
  ```
  N_{event,i} ~ N_event/N_spec.
  ```
  We obtain
  ```
  \sum_{i=1}^{N_spec} (N_{event,i} * t_{event,linear} + N_{event,i} log N_{event,i} * t_{event,NlogN} + ...)
    ~ \sum_{i=1}^{N_spec} (N_event/N_spec * t_{event,linear} + N_event/N_spec log (N_event/N_spec) * t_{event,NlogN} + ...)
    = N_event*t_{event,linear} + N_event/N_spec \sum_{i=1}^{N_spec} (log (N_event/N_spec) * t_{event,NlogN} + ...).
    = N_event*t_{event,linear} + N_event (log (N_event/N_spec) * t_{event,NlogN} + ...).
  ```
  The term in parenthesis depends on `log (N_event/N_spec)` and *not* `log N_event` (similar for higher order terms).
  These terms are thus typically small and it is reasonable to absorb them into the linear term
  ```
    ~ N_event*t_event.
  ```
  If instead events are peaked in a subset of spectra we approximate `N_{event,i} ~ (0 or N_event/N_peak)`, the approximation works in a similar way.
- Loading large event files is a significant contribution to the overall reduction time.
  While the exact scaling of the new parallel event loader is unknown (no adequate parallel file system available), there is definitely a linearly scaling contribution that scales well with the number of cores and is thus already described by the `N_event*t_event` term.
  In addition to that, the other major factor is given by the upper limit of file system bandwidth.
  Basically, this is a limit to the number of events that can be loaded per second.
  This will also depend on whether or not compression is used in NeXus files.
  We model this limit in the equation with the term `N_event/bandwidth_max`.
- The time for reducing a spectrum will often depend linearly on the bin count.
  However, for a given reduction workflow the bin count does not vary much, so there is not need to express it explicitly.
