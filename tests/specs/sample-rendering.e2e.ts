import AppPage from '../pageobjects/mediview-3d.page';

// handle pixel jitter in 3D view
const THRESHOLD = 10; // percent

describe('mediview-3d', () => {
  it('should load and render a sample dataset', async () => {
    await AppPage.open();
    await AppPage.downloadProstateSample();
    await AppPage.waitForViews();
    await browser.pause(5000);

    expect(
      await browser.checkElement(
        await $('div[data-testid~="layout-grid"]'),
        'prostate_sample_views'
      )
    ).toBeLessThan(THRESHOLD);
  });
});
