import macro from '@kitware/vtk.js/macro';

import { AnnotationToolType } from '@/src/store/tools/types';
import vtkRulerWidget from '../RulerWidget';
import vtkRectangleLineRepresentation from './RectangleLineRepresentation';

export { InteractionState } from '../RulerWidget/behavior';

// ----------------------------------------------------------------------------
// Factory
// ----------------------------------------------------------------------------

function vtkRectangleWidget(publicAPI, model) {
  model.classHierarchy.push('vtkRectangleWidget');

  const superGetRepresentationsForViewType =
    publicAPI.getRepresentationsForViewType;
  publicAPI.getRepresentationsForViewType = () => {
    const reps = superGetRepresentationsForViewType();
    reps[1].builder = vtkRectangleLineRepresentation;
    reps[1].initialValues = {
      ...reps[1].initialValues,
      widgetAPI: model,
    };
    return reps;
  };
}

// ----------------------------------------------------------------------------

const DEFAULT_VALUES = {};

// ----------------------------------------------------------------------------

export function extend(publicAPI, model, initialValues = {}) {
  Object.assign(model, DEFAULT_VALUES, initialValues);

  vtkRulerWidget.extend(publicAPI, model, {
    ...initialValues,
    toolType: AnnotationToolType.Rectangle,
  });

  vtkRectangleWidget(publicAPI, model);
}

// ----------------------------------------------------------------------------

export const newInstance = macro.newInstance(extend, 'vtkRectangleWidget');

// ----------------------------------------------------------------------------

export default { newInstance, extend };
