# Xsuite: Developer Guide

## Custom Beam Elements

### Data Structure

Define beam element data using xobjects:

```python
import xobjects as xo
import xtrack as xt

class MyElement(xt.BeamElement):
    _xofields = {
        'k': xo.Float64,           # scalar field
        'length': xo.Float64,
        'data_array': xo.Float64[:],  # array field
        'order': xo.Int64,
    }
```

### Tracking Code (C kernel)

Write the C tracking code for the element:

```python
class MyElement(xt.BeamElement):
    _xofields = {
        'k': xo.Float64,
        'length': xo.Float64,
    }

    _extra_c_sources = ['''
    /*gpufun*/
    void MyElement_track_local_particle(
            MyElementData el,
            LocalParticle* part0) {

        double const k = MyElementData_get_k(el);
        double const length = MyElementData_get_length(el);

        //start_per_particle_block (part0->part)
            double const x = LocalParticle_get_x(part);
            double const px = LocalParticle_get_px(part);

            // Apply some transformation
            double const new_px = px + k * x * length;

            LocalParticle_set_px(part, new_px);
            LocalParticle_add_to_s(part, length);
        //end_per_particle_block
    }
    ''']
```

### LocalParticle C API

Available getters/setters for the C tracking code:

```c
// Position and momentum
LocalParticle_get_x(part)       // horizontal position
LocalParticle_get_px(part)      // horizontal angle
LocalParticle_get_y(part)       // vertical position
LocalParticle_get_py(part)      // vertical angle
LocalParticle_get_zeta(part)    // longitudinal coordinate
LocalParticle_get_delta(part)   // momentum deviation
LocalParticle_get_pzeta(part)   // pzeta

// Energy-related
LocalParticle_get_energy0(part)  // reference energy
LocalParticle_get_p0c(part)      // reference momentum
LocalParticle_get_gamma0(part)   // reference gamma
LocalParticle_get_beta0(part)    // reference beta
LocalParticle_get_mass0(part)    // reference mass
LocalParticle_get_q0(part)       // reference charge
LocalParticle_get_chi(part)      // charge ratio

// State
LocalParticle_get_state(part)    // particle state
LocalParticle_get_at_turn(part)  // current turn
LocalParticle_get_particle_id(part) // particle ID

// Setters
LocalParticle_set_x(part, value)
LocalParticle_set_px(part, value)
LocalParticle_add_to_x(part, value)    // increment
LocalParticle_add_to_px(part, value)
LocalParticle_add_to_s(part, value)    // advance s position
LocalParticle_add_to_energy(part, value) // add energy

// Kill particle
LocalParticle_set_state(part, -1)  // mark as lost
```

## Internal Records

Record data from within beam elements during tracking:

```python
class MyRecordElement(xt.BeamElement):
    _xofields = {
        'threshold': xo.Float64,
    }

    # Define record structure
    class MyRecord(xo.HybridClass):
        _xofields = {
            'x_at_record': xo.Float64[:],
            'y_at_record': xo.Float64[:],
            'particle_id': xo.Int64[:],
            'at_turn': xo.Int64[:],
        }

    _internal_record_class = MyRecord

    _extra_c_sources = ['''
    /*gpufun*/
    void MyRecordElement_track_local_particle(
            MyRecordElementData el,
            LocalParticle* part0) {

        double threshold = MyRecordElementData_get_threshold(el);

        //start_per_particle_block (part0->part)
            double x = LocalParticle_get_x(part);

            if (fabs(x) > threshold) {
                // Record data
                MyRecordData record = MyRecordElementData_getp_internal_record(el, part);
                if (record) {
                    int64_t i_slot = MyRecordData_append_x_at_record(record);
                    MyRecordData_set_x_at_record(record, i_slot, x);
                    MyRecordData_set_y_at_record(record, i_slot,
                        LocalParticle_get_y(part));
                    MyRecordData_set_particle_id(record, i_slot,
                        LocalParticle_get_particle_id(part));
                    MyRecordData_set_at_turn(record, i_slot,
                        LocalParticle_get_at_turn(part));
                }
            }
        //end_per_particle_block
    }
    ''']

# Usage
line.insert_element(element=MyRecordElement(threshold=1e-3), name='recorder')
line.track(particles, num_turns=100)

# Access records
record = line.record_last_track
record.x_at_record
record.y_at_record
```

## Lost Particle State Codes

Negative state values indicate how particles were lost:

- `state > 0`: alive
- `state == 0`: lost on aperture
- `state == -1`: generic loss
- `state == -2`: lost due to long_limit
- `state == -333`: absorbed in collimator (xcoll)
- Custom codes can be defined for custom elements

## Multiplatform Programming with XObjects

### Define Data Structures

```python
import xobjects as xo

class DataStructure(xo.Struct):
    a = xo.Float64[:]
    b = xo.Float64[:]
    c = xo.Float64[:]
    s = xo.Float64
```

### Allocate on CPU or GPU

```python
ctx = xo.ContextCpu()          # CPU
# ctx = xo.ContextCupy()       # NVIDIA GPU
# ctx = xo.ContextPyopencl()   # OpenCL GPU

obj = DataStructure(_context=ctx, a=[1,2,3], b=[4,5,6], c=[0,0,0], s=0)
```

### Access Data

```python
print(obj.a[2])    # read
obj.a[2] = 10      # write

# As numpy-like array (view, not copy)
arr = obj.a.to_nplike()
arr[:] = obj.b.to_nplike() - 1     # numpy operations modify underlying data
```

### Custom C Kernels

```python
src = '''
/*gpukern*/
void myprod(DataStructure ob, int nelem){
    for (int ii=0; ii<nelem; ii++){ //vectorize_over ii nelem
        double a_ii = DataStructure_get_a(ob, ii);
        double b_ii = DataStructure_get_b(ob, ii);
        DataStructure_set_c(ob, ii, a_ii * b_ii);
    } //end_vectorize
}
'''

ctx.add_kernels(
    sources=[src],
    kernels={'myprod': xo.Kernel(
        args=[xo.Arg(DataStructure, name='ob'),
              xo.Arg(xo.Int32, name='nelem')],
        n_threads='nelem')})

ctx.kernels.myprod(ob=obj, nelem=len(obj.a))
```

### C Annotations

- `/*gpukern*/` - marks a kernel function (parallelized on GPU)
- `/*gpufun*/` - marks a device function (not a kernel entry point)
- `//vectorize_over ii nelem` ... `//end_vectorize` - loop parallelized on GPU
- `/*gpuglmem*/` - global memory pointer

### HybridClass (Python + C dual representation)

```python
class MyClass(xo.HybridClass):
    _xofields = {
        'field_a': xo.Float64,
        'field_b': xo.Float64[:],
    }

    def my_method(self):
        return self.field_a + sum(self.field_b)
```

### Memory Management

```python
# Contexts and buffers
ctx = xo.ContextCpu()
buffer = ctx.new_buffer(capacity=1024)

# Allocate in specific buffer
obj1 = DataStructure(_buffer=buffer, a=[1,2], b=[3,4], c=[0,0], s=0)
obj2 = DataStructure(_buffer=buffer, a=[5,6], b=[7,8], c=[0,0], s=0)

# Move between contexts
obj1.move(_context=xo.ContextCupy())
```

## Testing

```python
# Run xsuite tests
import xtrack
xtrack.test()

# Run specific tests
# pytest xtrack/tests/test_twiss.py -v
```
